import streamlit as st
import os
import time
import tempfile
import base64
from main import (
    load_models,
    process_video,
    convert_video_for_browser
)

# -------------------------------------------------------
# 🎨 PAGE SETUP
# -------------------------------------------------------
st.set_page_config(
    page_title="ANPR Vision AI",
    page_icon="🚗",
    layout="wide"
)

# -------------------------------------------------------
# 🌈 GLOBAL PAGE RESIZE
# -------------------------------------------------------
st.markdown("""
<style>
/* 🌟 Shrink the whole page width */
.main {
    max-width: 750px;         /* Adjust page width here */
    margin-left: auto;
    margin-right: auto;
}

/* Center everything */
.block-container {
    padding-top: 1rem;
    margin: auto;
}

/* ---- UI STYLING ---- */
html, body {
    background: linear-gradient(135deg, #f0f9ff 0%, #cbebff 40%, #a1dbff 100%);
}

h1.title {
    font-size: 2.5rem !important;
    text-align: center;
    color: #0A3D62;
    font-weight: 800;
    padding-bottom: 10px;
}

.upload-box {
    padding: 25px;
    border-radius: 18px;
    background: #ffffffaa;
    backdrop-filter: blur(8px);
    border: 2px dashed #1B98F5;
    text-align: center;
    transition: 0.3s ease-in-out;
}

.upload-box:hover {
    border-color: #0F74BD;
    background: #ffffffcc;
}

.step-header {
    font-size: 1.4rem;
    font-weight: 700;
    padding: 12px 15px;
    background: linear-gradient(90deg, #2980B9, #6DD5FA);
    color: white;
    border-radius: 10px;
    margin-top: 30px;
}

.result-box {
    background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
    padding: 20px;
    border-radius: 15px;
    color: #054a29;
    font-weight: 600;
    box-shadow: 0 4px 10px #00000030;
}

.video-card {
    padding: 15px;
    border-radius: 15px;
    background: #ffffffdd;
    backdrop-filter: blur(6px);
    margin-top: 15px;
    border-left: 6px solid #2980B9;
    box-shadow: 0 4px 15px #00000025;
}

.stButton>button {
    background: linear-gradient(90deg, #1B98F5, #6DD5FA);
    color: white;
    border-radius: 12px;
    padding: 14px;
    font-size: 18px;
    font-weight: 700;
    border: none;
    transition: 0.2s ease-in-out;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #1B98F5, #4BCFFA);
    cursor: pointer;
}

/* Video containers – auto-resize */
.video-container, .video-output {
    text-align: center;
    margin-top: 10px;
}

video {
    width: 100% !important;
    max-width: 550px;     /* shrink the actual video size */
    border-radius: 12px;
    box-shadow: 0 4px 12px #00000030;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# 🌟 HEADER TITLE
# -------------------------------------------------------
st.markdown("<h1 class='title'>🚗 ANPR – Automatic Number Plate Recognition</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:16px;'>YOLOv8 + EasyOCR | Smart Video Processing System</p>", unsafe_allow_html=True)

# -------------------------------------------------------
# 📤 STEP 1 — FILE UPLOAD
# -------------------------------------------------------
st.markdown("<div class='step-header'>📤 Step 1: Upload Your Video File</div>", unsafe_allow_html=True)
st.markdown("<div class='upload-box'>Drag & Drop your MP4/MOV/AVI video or browse</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["mp4", "mov", "avi", "mkv"])

# ---------- Uploaded Video Preview ----------
if uploaded_file:
    st.markdown("<div class='video-card'>🎞️ Uploaded Video Preview</div>", unsafe_allow_html=True)

    # Convert video to base64
    file_bytes = uploaded_file.read()
    video_base64 = base64.b64encode(file_bytes).decode("utf-8")

    st.markdown("<div class='video-container'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <video controls>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        """,
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------
    # ⚙️ STEP 2 — PROCESSING
    # -------------------------------------------------------
    st.markdown("<div class='step-header'>⚙️ Step 2: Process Your Video</div>", unsafe_allow_html=True)

    if st.button("🚀 Start ANPR Processing"):

        with st.spinner("🔄 Loading AI models…"):
            model, reader = load_models()

        # Save input file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(file_bytes)
            input_path = tmp.name

        temp_output = tempfile.mktemp(suffix="_temp.mp4")
        final_output = tempfile.mktemp(suffix=".mp4")

        progress = st.progress(0)
        status = st.empty()

        def update_progress(frame, total):
            progress.progress(frame / total)
            status.text(f"Processing frame {frame} / {total}…")

        st.info("🧠 Running YOLO + OCR…")
        success, plates = process_video(
            input_path,
            temp_output,
            model,
            reader,
            callback=update_progress
        )

        if success:
            st.success("🎉 Processing complete! Converting for playback…")

            ok, err = convert_video_for_browser(temp_output, final_output)
            output_file = final_output if ok else temp_output

            # -------------------------------------------------------
            # 📥 STEP 3 — PREVIEW OUTPUT
            # -------------------------------------------------------
            st.markdown("<div class='step-header'>📥 Step 3: Download & Preview</div>",
                        unsafe_allow_html=True)
            st.markdown("<div class='video-card'>🎬 Processed Video Preview</div>",
                        unsafe_allow_html=True)

            with open(output_file, "rb") as f:
                output_bytes = f.read()

            output_base64 = base64.b64encode(output_bytes).decode("utf-8")

            st.markdown("<div class='video-output'>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <video controls>
                    <source src="data:video/mp4;base64,{output_base64}" type="video/mp4">
                </video>
                """,
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # -------------------------------------------------------
            # 📥 DOWNLOAD
            # -------------------------------------------------------
            st.download_button(
                "⬇️ Download Processed Video",
                output_bytes,
                file_name=f"ANPR_output_{int(time.time())}.mp4",
                mime="video/mp4",
            )

        

        else:
            st.error(f"❌ Error: {plates}")
