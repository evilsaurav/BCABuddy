import streamlit as st
import requests

# -------------------------
# App Config
# -------------------------
st.set_page_config(
    page_title="BCABuddy",
    page_icon="🤝",
    layout="centered"
)

BACKEND_URL = "http://127.0.0.1:8000/chat"

# -------------------------
# Session State
# -------------------------
if "mode" not in st.session_state:
    st.session_state.mode = None

# -------------------------
# Header / Intro
# -------------------------
st.title("🤝 BCABuddy")
st.markdown(
    """
**Hi! I’m BCABuddy — BCA life ka emotional support AI.**  
Assignments, PYQ, Notes, Viva, Lab, Summary — bol kya chahiye? 😄
"""
)

# -------------------------
# Mode Chips
# -------------------------
st.subheader("Choose a mode")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📘 Assignment"):
        st.session_state.mode = "Assignment"
with col2:
    if st.button("🎯 PYQ"):
        st.session_state.mode = "PYQ"
with col3:
    if st.button("📚 Notes"):
        st.session_state.mode = "Notes"

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("🎙 Viva"):
        st.session_state.mode = "Viva"
with col5:
    if st.button("🧪 Lab"):
        st.session_state.mode = "Lab"
with col6:
    if st.button("✍ Summary"):
        st.session_state.mode = "Summary"

if st.session_state.mode:
    st.success(f"Selected Mode: {st.session_state.mode}")

# -------------------------
# Chat Input
# -------------------------
st.divider()
user_message = st.text_area(
    "Ask your question",
    placeholder="Example: Explain OS deadlock for 10 marks",
    height=100
)

language = st.selectbox(
    "Language",
    ["hinglish", "english"],
    index=0
)

# -------------------------
# Send Button
# -------------------------
if st.button("Ask BCABuddy"):
    if not st.session_state.mode:
        st.warning("Please select a mode first 👆")
    elif not user_message.strip():
        st.warning("Please type a question 🙂")
    else:
        payload = {
            "message": user_message,
            "mode": st.session_state.mode,
            "language": language
        }

        try:
            with st.spinner("BCABuddy soch raha hai..."):
                response = requests.post(BACKEND_URL, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()

            st.markdown("### 💬 BCABuddy says:")
            st.write(data.get("reply", ""))

        except requests.exceptions.RequestException as e:
            st.error("Backend se connect nahi ho pa raha 😕")
            st.code(str(e))
