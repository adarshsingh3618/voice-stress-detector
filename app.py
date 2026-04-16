import streamlit as st

from tabs import upload, record, realtime

st.set_page_config(
    page_title="Voice Stress Detection",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Voice Stress Detection Dashboard")

tab1, tab2, tab3 = st.tabs([
    "📤 Upload Audio",
    "🎙️ Record",
    "⚡ Real-Time"
])

with tab1:
    record.show()

with tab2:
    upload.show()

with tab3:
    realtime.show()