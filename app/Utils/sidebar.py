import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("📌 Menu")

        st.subheader("Main")
        if st.button("📊 Dashboard"):
            st.switch_page("pages/1_Dashboard.py")
        if st.button("📈 Analytics"):
            st.switch_page("pages/2_Analytics.py")
        if st.button("⚙️ Settings"):
            st.switch_page("pages/3_Settings.py")
        if st.button("🤖 AI Assistance"):
            st.switch_page("pages/4_Ai.py")

        st.markdown("---")
        st.subheader("Users & Access")
        if st.button("👤 View Users"):
            st.session_state["show_users"] = True
        if st.button("🔐 Login"):
            st.switch_page("pages/login.py")