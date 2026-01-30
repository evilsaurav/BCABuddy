import streamlit as st
import requests

st.set_page_config(page_title="BCABuddy", page_icon="🎓")
st.title("🎓 BCABuddy AI")

# Sidebar
with st.sidebar:
    st.header("Settings")
    lang = st.selectbox("Language", ["Hinglish", "English"])
    size = st.selectbox("Length", ["Short", "Medium", "Long"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask me..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API Call
    payload = {"message": prompt, "language": lang, "mode": size}
    res = requests.post("http://127.0.0.1:8000/chat", json=payload).json()
    
    ans = res.get("reply")
    st.session_state.messages.append({"role": "assistant", "content": ans})
    with st.chat_message("assistant"):
        st.markdown(ans)