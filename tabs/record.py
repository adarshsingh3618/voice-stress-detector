import streamlit as st
import os
from main import predict

from utils.gemini_utils import (
    configure_gemini,
    analyze_text_stress,
    generate_companion_response
)
from utils.fusion_utils import calculate_final_stress, get_stress_level

TEMP_RECORD = "temp_record.wav"


def show():
    st.header("🎙️ Guided Stress Assessment")
    st.write("Answer the questions below and record your voice.")

    # ----------------------------------------
    # SESSION STATE INIT
    # ----------------------------------------
    if "answers" not in st.session_state:
        st.session_state.answers = ["", "", ""]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            ("assistant", "Hey… I’m here with you. Want to talk about what’s going on?")
        ]

    # ----------------------------------------
    # QUESTIONS
    # ----------------------------------------
    questions = [
        "How has your day been so far?",
        "Are you feeling overwhelmed or just tired?",
        "What is bothering you the most right now?"
    ]

    st.subheader("💬 Answer these questions")

    for i, q in enumerate(questions):
        st.session_state.answers[i] = st.text_input(
            f"{i+1}. {q}",
            value=st.session_state.answers[i]
        )

    # ----------------------------------------
    # CONTROLLED SPEECH
    # ----------------------------------------
    st.info("🎙️ Please also say this sentence while recording:")
    st.code("I am speaking clearly and calmly about my current situation.")

    # ----------------------------------------
    # AUDIO INPUT
    # ----------------------------------------
    audio_file = st.audio_input("🎙️ Record your voice")

    # Gemini client
    client = configure_gemini()

    if audio_file is not None:
        st.audio(audio_file)

        with open(TEMP_RECORD, "wb") as f:
            f.write(audio_file.read())

        if st.button("🔍 Analyze Stress"):

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

            # Save for chat
            st.session_state.final_score = final_score
            st.session_state.level = level
            st.session_state.client = client

            # ----------------------------------------
            # RESULTS
            # ----------------------------------------
            st.subheader("🧠 Final Stress Analysis")

            st.write(f"🎙️ Voice Score: {voice_score}/10")
            st.write(f"💬 Text Score (avg): {text_score}/10")
            st.write(f"⚡ Final Score: {final_score}/10")
            st.write(f"📊 Stress Level: {level}")
            st.write(f"🧠 Dominant Emotion: {emotion}")

            if level == "Low":
                st.success("You're doing well 👍 Keep it up!")
            elif level == "Moderate":
                st.warning("You're a bit stressed. Try taking a short break 🧘")
            elif level == "High":
                st.error("You're quite stressed ⚠️ Consider relaxing activities")
            else:
                st.error("Extreme stress detected 🚨 Please consider talking to someone")

    # ----------------------------------------
    # 🖤 COMPANION MODE (FIXED)
    # ----------------------------------------
    if "level" in st.session_state and st.session_state.level in ["Moderate", "High", "Extreme"]:

        st.subheader("🖤 AI Companion")

        # Show chat history (correct order)
        for role, msg in st.session_state.chat_history:
            st.chat_message(role).write(msg)

        # Chat input (no repeat bug)
        user_input = st.chat_input("Say something...")

        if user_input:
            # Add user message
            st.session_state.chat_history.append(("user", user_input))

            # Generate response
            reply = generate_companion_response(
                st.session_state.client,
                st.session_state.chat_history,
                st.session_state.final_score,
                st.session_state.level
            )

            # ----------------------------------------
            # 🚫 ANTI-REPETITION GUARD (ADD HERE)
            # ----------------------------------------
            if len(st.session_state.chat_history) > 1:
                last_reply = st.session_state.chat_history[-1][1]
                if reply == last_reply:
                    reply += "\n\nTell me a bit more about what's making you feel this way."

            # Add assistant reply
            st.session_state.chat_history.append(("assistant", reply))

            # Refresh UI
            st.rerun()

    # ----------------------------------------
    # CLEANUP
    # ----------------------------------------
    if os.path.exists(TEMP_RECORD):
        os.remove(TEMP_RECORD)