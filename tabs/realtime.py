import streamlit as st
import numpy as np
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
from main import predict
import tempfile
import soundfile as sf
import time
import datetime

from utils.db_auth import save_stress  # ✅ DB integration


def show():

    st.markdown('<div class="soft-card"><h2>⚡ Passive Stress Monitor</h2></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="soft-card">
        System is continuously listening in the background and updating your stress level every few seconds.
    </div>
    """, unsafe_allow_html=True)

    # ---------------- SESSION STATE ---------------- #
    if "last_update" not in st.session_state:
        st.session_state.last_update = time.time()

    if "status" not in st.session_state:
        st.session_state.status = "Listening..."
        st.session_state.confidence = 0.0

    if "buffer" not in st.session_state:
        st.session_state.buffer = []

    UPDATE_INTERVAL = 15  # seconds

    # ---------------- AUDIO PROCESSOR ---------------- #
    class AudioProcessor(AudioProcessorBase):

        def recv(self, frame):
            audio = frame.to_ndarray()

            # Convert stereo → mono
            if len(audio.shape) > 1:
                audio = np.mean(audio, axis=1)

            # Append audio buffer
            st.session_state.buffer.extend(audio.tolist())

            current_time = time.time()

            # Run prediction periodically
            if current_time - st.session_state.last_update > UPDATE_INTERVAL:

                st.session_state.last_update = current_time

                # Take last chunk (~3 sec)
                chunk = np.array(st.session_state.buffer[-48000:])

                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    sf.write(tmp.name, chunk, 16000)

                    try:
                        result, confidence, voice_score = predict(tmp.name)

                        st.session_state.status = result
                        st.session_state.confidence = confidence

                        # ---------------- SAVE DATA ---------------- #
                        entry = {
                            "time": datetime.datetime.now().strftime("%H:%M:%S"),
                            "voice_score": voice_score,
                            "text_score": 0,
                            "final_score": voice_score
                        }

                        # Save in session (dashboard)
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
                        pass

            return frame

    # ---------------- START STREAM ---------------- #
    webrtc_streamer(
        key="silent-monitor",
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
    )

    # ---------------- OUTPUT ---------------- #
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.subheader("🧠 Current Stress State")

    if st.session_state.status == "Stress":
        st.error(f"⚠️ Stress Detected ({st.session_state.confidence:.2f})")
    elif st.session_state.status == "No Stress":
        st.success(f"✅ Calm State ({st.session_state.confidence:.2f})")
    else:
        st.info("Listening...")

    st.markdown('</div>', unsafe_allow_html=True)