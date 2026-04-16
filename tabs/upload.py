from utils.gemini_utils import configure_gemini, analyze_text_stress
from utils.fusion_utils import calculate_final_stress, get_stress_level
import streamlit as st
import os
from main import predict
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

        # 📊 Waveform
        y = load_audio_for_waveform(TEMP_UPLOAD)
        st.subheader("Waveform")
        st.line_chart(y)

        # 🧠 Initialize Gemini
        client = configure_gemini()

        # 💬 User input
        user_text = st.text_input("How are you feeling right now?")

        # 🔍 Analyze button
        if st.button("🔍 Analyze Stress"):

            # 🎙️ Voice analysis
            result, confidence, voice_score = predict(TEMP_UPLOAD)

            # 💬 Text analysis
            if user_text:
                text_data = analyze_text_stress(client, user_text)
                text_score = text_data["stress_score"]

                # ⚔️ Fusion
                final_score = calculate_final_stress(text_score, voice_score)
                level = get_stress_level(final_score)

                # 📊 Display results
                st.subheader("🧠 Final Stress Analysis")

                st.write(f"🎙️ Voice Score: {voice_score}/10")
                st.write(f"💬 Text Score: {text_score}/10")
                st.write(f"⚡ Final Score: {final_score}/10")
                st.write(f"📊 Stress Level: {level}")

                # 🎯 Feedback
                if level == "Low":
                    st.success("You're doing well 👍")
                elif level == "Moderate":
                    st.warning("Take a short break 🧘")
                elif level == "High":
                    st.error("You're quite stressed ⚠️")
                else:
                    st.error("Extreme stress detected 🚨 Consider support")

            else:
                st.warning("Please enter how you're feeling.")

        # 🧹 Cleanup
        if os.path.exists(TEMP_UPLOAD):
            os.remove(TEMP_UPLOAD)