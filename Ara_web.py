import streamlit as st
import requests
import os
from dotenv import load_dotenv
from groq import Groq
from duckduckgo_search import DDGS

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")



def search_web(query):
    """Search the web for current information"""
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=3)
        
        if results:
            response = "Here's what I found:\n\n"
            for i, result in enumerate(results, 1):
                response += f"{i}. **{result['title']}**\n"
                response += f"   {result['body']}\n\n"
            return response
        else:
            return "No search results found."
    except:
        return "Could not search the web right now."
    
     

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        return f"Weather in {city}: {desc}, Temperature: {temp}°C, Humidity: {humidity}%"
    else:
        return f"Sorry, I couldn't find weather for {city}!"

st.title("Ara- Your AI Assistant")
st.caption("Ask me anything!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant named Ara. You are friendly, smart and kind."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    # check if user is asking for current\recent info
    search_keywords=["news", "current", "latest", "today", "recent", "2024", "2025", "2026", "what happened"]
    if any(keyword in user_input.lower() for keyword in search_keywords):
        search_result=search_web(user_input)
        with st.chat_message("assistant"):
            st.write(search_result)
        Continue
    

    if "weather" in user_input.lower():
        city = user_input.lower().replace("weather", "").replace("in", "").replace("of", "").strip()
        city = city if city else "London"
        reply = get_weather(city) + " 🌤️"
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)