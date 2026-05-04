import streamlit as st
import os
import datetime

from main import predict

from utils.gemini_utils import (
    configure_gemini,
    analyze_text_stress,
    generate_companion_response
)

from utils.fusion_utils import calculate_final_stress, get_stress_level
from utils.db_auth import save_stress  # ✅ DB integration

TEMP_RECORD = "temp_record.wav"


def show():

    st.markdown('<div class="soft-card"><h2>🎙️ Guided Stress Assessment</h2></div>', unsafe_allow_html=True)

    # ---------------- SESSION STATE ---------------- #
    if "answers" not in st.session_state:
        st.session_state.answers = ["", "", ""]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            ("assistant", "I'm here with you. Tell me what's going on.")
        ]

    # ---------------- QUESTIONS ---------------- #
    questions = [
        "How has your day been so far?",
        "Are you feeling overwhelmed or just tired?",
        "What is bothering you the most right now?"
    ]

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.subheader("💬 Answer these questions")

    for i, q in enumerate(questions):
        st.session_state.answers[i] = st.text_input(
            f"{i+1}. {q}",
            value=st.session_state.answers[i]
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- CONTROLLED SPEECH ---------------- #
    st.markdown("""
    <div class="soft-card">
        <b>🎙️ Please say this while recording:</b>
        <br><br>
        <code>I am speaking clearly and calmly about my current situation.</code>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- AUDIO INPUT ---------------- #
    audio_file = st.audio_input("🎙️ Record your voice")

    client = configure_gemini()

    if audio_file is not None:
        st.audio(audio_file)

        with open(TEMP_RECORD, "wb") as f:
            f.write(audio_file.read())

        if st.button("🔍 Analyze Stress"):

            with st.spinner("Analyzing your emotional state..."):

                # 🎙️ Voice
                result, confidence, voice_score = predict(TEMP_RECORD)

                # 💬 Text
                text_scores = []
                emotions = []

                for ans in st.session_state.answers:
                    if ans.strip():
                        data = analyze_text_stress(client, ans)
                        text_scores.append(data["stress_score"])
                        emotions.append(data["emotion"])

                if not text_scores:
                    st.warning("Please answer at least one question.")
                    return

                text_score = round(sum(text_scores) / len(text_scores), 1)
                emotion = max(set(emotions), key=emotions.count)

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

                # Save in session
                if "history" not in st.session_state:
                    st.session_state.history = []

                st.session_state.history.append(entry)

                # 🔥 Save in DB
                save_stress(
                    st.session_state.user,
                    entry["time"],
                    entry["voice_score"],
                    entry["text_score"],
                    entry["final_score"]
                )

                # Save for AI companion
                st.session_state.final_score = final_score
                st.session_state.level = level
                st.session_state.client = client

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

            st.markdown(f"""
            <b>📊 Stress Level:</b> {level} <br>
            <b>🧠 Emotion:</b> {emotion}
            """, unsafe_allow_html=True)

            if level == "Low":
                st.success("You're doing well 👍")
            elif level == "Moderate":
                st.warning("Take a small break 🧘")
            elif level == "High":
                st.error("High stress detected ⚠️")
            else:
                st.error("Extreme stress 🚨 Consider support")

            st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- AI COMPANION ---------------- #
    if "level" in st.session_state and st.session_state.level in ["Moderate", "High", "Extreme"]:

        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.subheader("🖤 AI Companion")

        for role, msg in st.session_state.chat_history:
            st.chat_message(role).write(msg)

        user_input = st.chat_input("Talk to me...")

        if user_input:
            st.session_state.chat_history.append(("user", user_input))

            reply = generate_companion_response(
                st.session_state.client,
                st.session_state.chat_history,
                st.session_state.final_score,
                st.session_state.level
            )

            # Anti repetition
            if len(st.session_state.chat_history) > 1:
                last_reply = st.session_state.chat_history[-1][1]
                if reply == last_reply:
                    reply += "\nTell me more about what's on your mind."

            st.session_state.chat_history.append(("assistant", reply))
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- CLEANUP ---------------- #
    if os.path.exists(TEMP_RECORD):
        os.remove(TEMP_RECORD)