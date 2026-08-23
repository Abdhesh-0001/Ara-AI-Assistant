import streamlit as st
from groq import Groq
import json
import os
import random

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_chat_history(filename="chat_history.json"):
    try:
        if os.path.exists(filename):
            with open(filename) as f:
                return json.load(f)
    except Exception:
        pass
    return []
        
def save_chat_history(history, filename="chat_history.json"):
    try:
        with open(filename, "w") as f:
            json.dump(history, f)
    except Exception as e:
        print(f"error saving: {e}")

def get_joke():
    jokes = [
        "Why did AI go to school? To improve its deep learning!",
        "Why do programmers like dark mode? Because light attracts bugs!"
    ]
    
    return random.choice(jokes)

def chat_with_groq(messages):
    system_msg = {
        "role": "system",
        "content": "You are Ara, a helpful AI assistant. Be concise and friendly."
    }
    all_msgs = [system_msg] + messages
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=all_msgs
    )
    return response.choices[0].message.content

if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

st.title("Ara AI Assistant")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle user input
user_input = st.chat_input("You: ")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    

    def get_groq_messages(messages):
        """Filter out system commands before sending to Groq"""
        filtered = []
        for msg in messages:
            content = msg["content"].lower()
            if "joke" not in content and "riddle" not in content:
                filtered.append(msg)
        return filtered
    if "joke" in user_input.lower():
        reply = get_joke()
    elif "riddle" in user_input.lower():
        reply = "I have cities but no houses. What am I?"
    else:
        reply = chat_with_groq(get_groq_messages(st.session_state.messages))
        
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
        
    with st.chat_message("assistant"):
        st.write(reply)
        
    save_chat_history(st.session_state.messages)