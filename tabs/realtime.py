import streamlit as st
import numpy as np
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
from main import predict
import tempfile
import soundfile as sf
import time


def show():
    st.header("⚡ Real-Time Stress Monitoring")

    st.info("System is continuously analyzing your voice...")

    # Initialize session state
    if "result" not in st.session_state:
        st.session_state.result = "Waiting..."
        st.session_state.confidence = 0.0
        st.session_state.history = []

    # 🎙️ Hidden audio processor
    class AudioProcessor(AudioProcessorBase):
        def recv(self, frame):
            audio = frame.to_ndarray()

            # Convert stereo → mono
            if len(audio.shape) > 1:
                audio = np.mean(audio, axis=1)

            # Save temp chunk
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                sf.write(tmp.name, audio, 16000)

                try:
                    result, confidence = predict(tmp.name)

                    st.session_state.result = result
                    st.session_state.confidence = confidence

                    # 📊 Store history (limit size)
                    value = confidence if result == "Stress" else 0
                    st.session_state.history.append(value)

                    if len(st.session_state.history) > 50:
                        st.session_state.history.pop(0)

                except Exception:
                    pass

            return frame

    # Start WebRTC (no UI controls)
    webrtc_streamer(
        key="stress-monitor",
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
    )

    # 🔥 Live Status
    st.subheader("🧠 Current Status")

    if st.session_state.result == "Stress":
        st.error(f"⚠️ Stress Detected ({st.session_state.confidence:.2f})")
    elif st.session_state.result == "No Stress":
        st.success(f"✅ No Stress ({st.session_state.confidence:.2f})")
    else:
        st.info("Listening...")

    # 📊 Live Graph
    st.subheader("📈 Stress Trend (Real-Time)")

    if st.session_state.history:
        st.line_chart(st.session_state.history)
    else:
        st.write("No data yet... start speaking 🎙️")