import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq


st.set_page_config(page_title="Alethia", page_icon="✨")
st.title("Alethia")
st.markdown("Hello! I’m Alethia, your intelligent personal assistant. How can I help you today?")


if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

if st.session_state["api_key"] == "":
    col1, col2 = st.columns([80, 20])
    with col1:
        input_api_key = st.text_input(
            "API Key",
            type="password",
            label_visibility="collapsed",
            placeholder="Type your Groq API key here...",
        )
    with col2:
        if st.button("Submit"):
            if input_api_key:
                st.session_state["api_key"] = input_api_key
                st.rerun()
            else:
                st.warning("Please enter an API Key first.")
    st.stop()


try:
    client = ChatGroq(
        model="openai/gpt-oss-120b", 
        api_key=st.session_state["api_key"]
    )
except Exception as e:
    st.error(f"Gagal menginisialisasi client Groq: {e}")
    st.stop()


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        SystemMessage(
            content="""You are Alethia, a helpful, friendly, and intelligent personal AI assistant.
Your name comes from the Greek word "aletheia", meaning truth.
You value accuracy, honesty, and clarity in every response.
If you do not know something or are uncertain, say so rather than inventing an answer.
Maintain a friendly, natural, and professional tone."""
)
    ]
chat_history = st.session_state["chat_history"]


for chat_msg in chat_history:
    if isinstance(chat_msg, HumanMessage):
        role = "user"
    elif isinstance(chat_msg, AIMessage):
        role = "assistant"
    else:
        continue
    with st.chat_message(role):
        st.markdown(chat_msg.content)


user_prompt = st.chat_input("Ask me anything...")

if user_prompt:
    chat_history.append(HumanMessage(content=user_prompt))
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.invoke(chat_history)
                st.markdown(response.content)
                chat_history.append(AIMessage(content=response.content))
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memanggil API: {e}")
