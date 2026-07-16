import streamlit as st
from groq import Groq
client = Groq(api_key="add-api-key-here ")

st.title("Chat with GPT")

if 'message' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("Enter your message:")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    completion = client.chat.completions.create(model="openai/gpt-oss-120b", messages = st.session_state.messages)


#reply = st.chat_message('user').markdown(prompt)
    reply = completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

