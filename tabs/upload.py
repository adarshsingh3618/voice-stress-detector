import streamlit as st
import os
from main import predict

# ✅ Import utils
from utils.audio_utils import load_audio_for_waveform

SAMPLE_RATE = 16000
TEMP_UPLOAD = "uploaded_audio.wav"


def show():
    st.header("📤 Upload Audio File")

    uploaded_file = st.file_uploader("Upload WAV or MP3", type=["wav", "mp3"])

    if uploaded_file:
        st.audio(uploaded_file)

        # 💾 Save uploaded file
        with open(TEMP_UPLOAD, "wb") as f:
            f.write(uploaded_file.getvalue())

        # 📊 Waveform using utils
        y = load_audio_for_waveform(TEMP_UPLOAD)

        st.subheader("Waveform")
        st.line_chart(y)

        # 🧠 Prediction
        if st.button("🔍 Analyze Audio"):
            result, confidence = predict(TEMP_UPLOAD)

            if result == "Stress":
                st.error(f"⚠️ Stress Detected (Confidence: {confidence:.2f})")
            else:
                st.success(f"✅ No Stress Detected (Confidence: {confidence:.2f})")

        # 🧹 Cleanup
        if os.path.exists(TEMP_UPLOAD):
            os.remove(TEMP_UPLOAD)