import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from tabs import upload, record, realtime
from utils.db_auth import (
    signup_user,
    login_user,
    create_tables,
    load_stress
)

# ---------------- INIT ---------------- #
create_tables()

st.set_page_config(
    page_title="AI Stress Intelligence",
    page_icon="🧠",
    layout="wide"
)

# ---------------- SESSION ---------------- #
if "history" not in st.session_state:
    st.session_state.history = []

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- AUTH ---------------- #
def auth_page():

    st.markdown("""
    <div style="text-align:center;">
        <h1>🧠 AI Stress Intelligence</h1>
        <p>Login to access your personal dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Signup"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            success, msg = login_user(username, password)

            if success:
                st.session_state.authenticated = True
                st.session_state.user = username
                st.session_state.history = load_stress(username)
                st.rerun()
            else:
                st.error(msg)

    with tab2:
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pass")

        if st.button("Signup"):
            success, msg = signup_user(new_user, new_pass)
            if success:
                st.success(msg)
            else:
                st.error(msg)


# ---------------- MAIN APP ---------------- #
def main_app():

    # Sidebar
    st.sidebar.markdown(f"👤 {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.history = []
        st.rerun()

    mode = st.sidebar.toggle("🌗 Dark Mode", value=False)

    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Dashboard", "📤 Upload", "🎙️ Record", "⚡ Real-Time"]
    )

    # ---------------- THEME ---------------- #
    if mode:
        gradient = "linear-gradient(180deg, #0F2027, #203A43)"
        text = "#EAF4FF"
        card = "rgba(20, 40, 60, 0.6)"
        shadow = "0 10px 30px rgba(0,0,0,0.6)"
        donut_colors = ["#7BBDE8", "#0A4174"]
        donut_text = "#EAF4FF"
    else:
        gradient = "linear-gradient(180deg, #EAF3F8, #CFE3F1)"
        text = "#1A2B3C"
        card = "rgba(255,255,255,0.85)"
        shadow = """
            10px 10px 25px rgba(0,0,0,0.1),
            -10px -10px 25px rgba(255,255,255,0.7)
        """
        donut_colors = ["#4E8EA2", "#D6E6F2"]
        donut_text = "#1A2B3C"

    # CSS
    st.markdown(f"""
    <style>
    .stApp {{
        background: {gradient};
        color: {text};
    }}
    .soft-card {{
        background: {card};
        border-radius: 28px;
        padding: 24px;
        box-shadow: {shadow};
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # ---------------- DONUT ---------------- #
    def donut_chart(value):
        fig, ax = plt.subplots()
        ax.pie(
            [value, 10 - value],
            colors=donut_colors,
            startangle=90,
            wedgeprops=dict(width=0.35)
        )
        ax.text(0, 0, f"{value}/10",
                ha='center', va='center',
                fontsize=18,
                color=donut_text)
        ax.axis('equal')
        fig.patch.set_alpha(0)
        return fig

    # ---------------- HEADER ---------------- #
    st.markdown("""
    <div class="soft-card">
        <h1>🧠 Stress Dashboard</h1>
        <p>Track your emotional patterns over time</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- DASHBOARD ---------------- #
    if page == "🏠 Dashboard":

        if st.session_state.history:

            df = pd.DataFrame(st.session_state.history)

            # ===== TOP ===== #
            latest = df.iloc[-1]

            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown('<div class="soft-card">', unsafe_allow_html=True)
                st.pyplot(donut_chart(latest["final_score"]))
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="soft-card">', unsafe_allow_html=True)
                st.write(f"🎙️ Voice: {latest['voice_score']}")
                st.write(f"💬 Text: {latest['text_score']}")
                st.write(f"⚡ Final: {latest['final_score']}")

                if latest["final_score"] >= 7:
                    st.error("⚠️ High Stress")
                elif latest["final_score"] >= 4:
                    st.warning("Moderate Stress")
                else:
                    st.success("Calm State")

                st.markdown('</div>', unsafe_allow_html=True)

            # ===== ANALYTICS PANEL ===== #
            st.markdown('<div class="soft-card">', unsafe_allow_html=True)
            st.subheader("📊 Analytics")

            avg = round(df["final_score"].mean(), 2)
            max_v = df["final_score"].max()
            min_v = df["final_score"].min()

            c1, c2, c3 = st.columns(3)
            c1.metric("Average", avg)
            c2.metric("Max", max_v)
            c3.metric("Min", min_v)

            # Trend
            if len(df) > 3:
                slope = np.polyfit(range(len(df)), df["final_score"], 1)[0]

                if slope > 0.1:
                    st.error("📈 Stress Increasing")
                elif slope < -0.1:
                    st.success("📉 Stress Decreasing")
                else:
                    st.info("➡️ Stress Stable")

            st.markdown('</div>', unsafe_allow_html=True)

            # ===== TIMELINE ===== #
            st.markdown('<div class="soft-card">', unsafe_allow_html=True)
            st.subheader("📈 Timeline")

            fig, ax = plt.subplots()
            ax.plot(df["final_score"], linewidth=3)
            ax.set_ylim(0, 10)
            fig.patch.set_alpha(0)
            st.pyplot(fig)

            st.markdown('</div>', unsafe_allow_html=True)

            # ===== HISTORY ===== #
            st.markdown('<div class="soft-card">', unsafe_allow_html=True)
            st.subheader("📋 History")

            min_score = st.slider("Min Score", 0.0, 10.0, 0.0)
            filtered = df[df["final_score"] >= min_score]

            st.dataframe(filtered, use_container_width=True)

            csv = filtered.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, "history.csv")

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.info("No data yet")

    elif page == "📤 Upload":
        upload.show()

    elif page == "🎙️ Record":
        record.show()

    elif page == "⚡ Real-Time":
        realtime.show()


# ---------------- ROUTER ---------------- #
if not st.session_state.authenticated:
    auth_page()
else:
    main_app()