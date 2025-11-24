import cv2
from ultralytics import YOLO
import easyocr
import subprocess
import os

# Load models
def load_models():
    yolo_model = YOLO("yolo.pt")
    ocr_reader = easyocr.Reader(['en'], gpu=False)
    return yolo_model, ocr_reader

# Clean OCR text
def clean_text(text):
    text = text.strip()
    text = ''.join([c if c.isalnum() else '.' for c in text])
    return text

# Convert video for browser playback
def convert_video_for_browser(input_path, output_path):
    try:
        cmd = [
            'ffmpeg', '-y',
            '-i', input_path,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            '-an',
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, f"ffmpeg error: {e.stderr}"
    except FileNotFoundError:
        return False, "ffmpeg not installed"
    except Exception as e:
        return False, str(e)

# Main ANPR video processor
def process_video(input_path, output_path, model, reader, callback=None):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise Exception("Error reading video file")

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    video_writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (w, h)
    )

    frame_count = 0
    detected_plates = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if callback:
            callback(frame_count, total_frames)

        # YOLO detection
        results = model(frame)
        annotated_frame = results[0].plot()

        # OCR processing
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            plate_crop = frame[y1:y2, x1:x2]

            ocr_result = reader.readtext(plate_crop, detail=0)
            text = clean_text(''.join(ocr_result))

            if text:
                detected_plates.add(text)

            # Draw text on frame
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.3
            thickness = 2
            text_color = (0, 255, 255)
            box_color = (0, 0, 0)
            margin_x, margin_y = 10, 6

            (tw, th), _ = cv2.getTextSize(text, font, font_scale, thickness)
            cv2.rectangle(
                annotated_frame,
                (x1, max(0, y1 - th - 2*margin_y)),
                (x1 + tw + 2*margin_x, y1),
                box_color,
                cv2.FILLED
            )
            cv2.putText(
                annotated_frame,
                text,
                (x1 + margin_x, max(0, y1 - margin_y)),
                font,
                font_scale,
                text_color,
                thickness
            )

        video_writer.write(annotated_frame)

    cap.release()
    video_writer.release()

    return True, detected_plates
