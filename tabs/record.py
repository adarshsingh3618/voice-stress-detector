import streamlit as st
import os
from main import predict

TEMP_RECORD = "temp_record.wav"


def show():
    st.header("🎙️ Record Your Voice")

    # 🎙️ Browser-based recording
    audio_file = st.audio_input("Click to record")

    if audio_file is not None:
        st.audio(audio_file)

        # 💾 Save audio
        with open(TEMP_RECORD, "wb") as f:
            f.write(audio_file.read())

        # 📊 Optional: show waveform (simple)
        st.subheader("Audio Captured ✅")

        # 🧠 Predict
        if st.button("🔍 Analyze Audio"):
            result, confidence = predict(TEMP_RECORD)

            if result == "Stress":
                st.error(f"⚠️ Stress Detected (Confidence: {confidence:.2f})")
            else:
                st.success(f"✅ No Stress Detected (Confidence: {confidence:.2f})")

        # 🧹 Cleanup
        if os.path.exists(TEMP_RECORD):
            os.remove(TEMP_RECORD)