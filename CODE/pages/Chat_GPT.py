"""
chat_GPT.py - AI chatbot page powered by Groq API
Restricts responses to application and project data only
"""
import streamlit as st
from groq import Groq

#load API key
client = Groq(api_key="Add API KEY HERE")

st.title("Chat Assistant")
st.caption("Ask me anything about this application or project data.")

#initialises chat history in session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

#display all previous messages in the chat
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

#get new message from user
prompt = st.chat_input("Enter your message:")

if prompt:
    #add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    #system prompt restricts the AI to project-related questions only
    system_prompt = [
        {
            "role": "system",
            "content": """ 
            You are a helpfull assistant for this dashboard.
            You can only answer questions about:
            -How to use the application
            -Cyber incidents data
            -IT tickets data
            -Datasets metadata
            If asked anything unrelated, politely say:
            'I can only answer question about this application and its data.'
            """
        }
    ]
    try:
        #send system prompt + full chat history to the model
        completion = client.chat.completions.create(model ="openai/gpt-oss-120b",messages = system_prompt + st.session_state.messages )

        #extract and display the reply
        reply = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
    except Exception as e:
        st.error(f"Error communicating with AI: {e}") #catch API errors or any exceptions errors
