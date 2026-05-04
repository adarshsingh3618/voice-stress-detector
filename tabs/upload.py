import streamlit as st
import os
import datetime

from main import predict
from utils.audio_utils import load_audio_for_waveform
from utils.gemini_utils import configure_gemini, analyze_text_stress
from utils.fusion_utils import calculate_final_stress, get_stress_level
from utils.db_auth import save_stress  # ✅ DB integration

TEMP_UPLOAD = "uploaded_audio.wav"


def show():

    st.markdown('<div class="soft-card"><h2>📤 Upload & Analyze Audio</h2></div>', unsafe_allow_html=True)

    # ---------------- FILE UPLOAD ---------------- #
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload WAV or MP3", type=["wav", "mp3"])

    if uploaded_file:
        st.audio(uploaded_file)

        # Save file
        with open(TEMP_UPLOAD, "wb") as f:
            f.write(uploaded_file.getvalue())

        # ---------------- WAVEFORM ---------------- #
        st.subheader("📊 Audio Waveform")

        try:
            y = load_audio_for_waveform(TEMP_UPLOAD)
            st.line_chart(y)
        except:
            st.warning("Could not generate waveform")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- TEXT INPUT ---------------- #
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)

    user_text = st.text_input("💬 How are you feeling right now?")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- ANALYSIS ---------------- #
    if uploaded_file and st.button("🔍 Analyze Stress"):

        client = configure_gemini()

        with st.spinner("Analyzing your emotional state..."):

            try:
                # 🎙️ Voice Analysis
                result, confidence, voice_score = predict(TEMP_UPLOAD)

                # 💬 Text Analysis
                if not user_text.strip():
                    st.warning("Please enter how you're feeling.")
                    return

                text_data = analyze_text_stress(client, user_text)
                text_score = text_data["stress_score"]

                # ⚔️ Fusion
                final_score = calculate_final_stress(text_score, voice_score)
                level = get_stress_level(final_score)

                # ---------------- SAVE DATA ---------------- #
                entry = {
                    "time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "voice_score": voice_score,
                    "text_score": text_score,
                    "final_score": final_score
                }

                # Save in session (for dashboard)
                if "history" not in st.session_state:
                    st.session_state.history = []

                st.session_state.history.append(entry)

                # 🔥 Save in DB (per user)
                save_stress(
                    st.session_state.user,
                    entry["time"],
                    entry["voice_score"],
                    entry["text_score"],
                    entry["final_score"]
                )

            except Exception:
                st.error("Error analyzing audio")
                return

        # ---------------- RESULTS UI ---------------- #
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.subheader("🧠 Stress Analysis Result")

        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
        <div class="soft-card">
            <h4>🎙️ Voice</h4>
            <h2>{voice_score}/10</h2>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="soft-card">
            <h4>💬 Text</h4>
            <h2>{text_score}/10</h2>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="soft-card">
            <h4>⚔️ Final</h4>
            <h2>{final_score}/10</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<b>📊 Stress Level:</b> {level}", unsafe_allow_html=True)

        # ---------------- FEEDBACK ---------------- #
        if level == "Low":
            st.success("You're doing well 👍")
        elif level == "Moderate":
            st.warning("Take a short break 🧘")
        elif level == "High":
            st.error("You're quite stressed ⚠️")
        else:
            st.error("Extreme stress detected 🚨 Consider support")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- CLEANUP ---------------- #
    if os.path.exists(TEMP_UPLOAD):
        os.remove(TEMP_UPLOAD)