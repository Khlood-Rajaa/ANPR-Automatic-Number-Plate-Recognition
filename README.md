#🚗 Automatic Number Plate Recognition (ANPR) System
📚 Overview
This project processes videos to detect license plates using YOLOv8, extracts text with EasyOCR, cleans the output, and writes the recognized plate numbers back onto each frame. It includes both a command-line script and a beautiful Streamlit web app for easy video processing.
✨ Features

🎯 YOLO-based license plate detection - Fast and accurate object detection
📝 EasyOCR text extraction - Multi-language OCR support
🧹 Auto-cleaning and formatting - Removes noise from OCR results
🎨 Bounding boxes + text overlays - Clear visual annotations
📹 Works with any video input - Supports MP4, AVI, MOV, MKV
🌐 Web interface with Streamlit - User-friendly GUI for non-technical users
🚀 Fast, lightweight, and beginner-friendly
🔧 Easy to customize - Adapt for any region or plate style
💾 Browser-compatible output - Videos play in any modern browser

🚀 Quick Start
Prerequisites
bash# Install Python dependencies
pip install opencv-python ultralytics easyocr streamlit

# Install ffmpeg (required for web app)
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
Usage
Option 1: Command Line (main.py)
bashpython main.py
How it works:
1️⃣ Load YOLO model for plate detection
pythonmodel = YOLO("yolo.pt")
2️⃣ Read input video
pythoncap = cv2.VideoCapture("anpr-demo-video.mp4")
3️⃣ Detect plates in each frame
pythonresults = model(frame)
4️⃣ Crop and apply OCR
pythonocr_result = reader.readtext(plate_crop, detail=0)
5️⃣ Clean OCR output
pythontext = clean_text(''.join(ocr_result))
6️⃣ Draw bounding box + text overlay
7️⃣ Save final processed video as anpr-output-easyocr.mp4
Option 2: Web Interface (app.py)
bashstreamlit run app.py
Then open your browser and:

📤 Upload your video file
⚙️ Click "Start Processing"
📥 Download the annotated video
🎬 Preview results in-browser

📁 Project Structure
anpr-project/
├── main.py              # CLI version - batch processing
├── app.py               # Streamlit web app
├── yolo.pt              # YOLO model weights (required)
├── anpr-demo-video.mp4  # Sample input video
└── README.md            # This file
🔧 How It Works (Detailed)
Detection Pipeline
python# 1. Initialize models
model = YOLO("yolo.pt")
reader = easyocr.Reader(['en'])

