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
        results = list(ddgs.text(query, max_results=3))
        
        if results:
            response = "🔍 **Latest Search Results:**\n\n"
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                body = result.get('body', 'No description')
                response += f"{i}. **{title}**\n"
                response += f"   {body}\n\n"
            print(f"✓ Search successful for: {query}")
            return response
        else:
            return "No search results found for that query."
    except Exception as e:
        print(f"✗ Search error: {str(e)}")
        return f"Search unavailable: {str(e)}"
    
     

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

    search_result = None
    weather_info = None
    
    # Check for weather query first
    if "weather" in user_input.lower():
        try:
            city = user_input.lower().replace("weather", "").replace("in", "").replace("of", "").strip()
            city = city if city else "London"
            weather_info = get_weather(city)
            print(f"Weather fetched: {city}")
        except Exception as e:
            print(f"Weather error: {str(e)}")
            weather_info = None
    
    # Always perform web search for latest information
    print(f"🔎 Searching web for: {user_input}")
    try:
        search_result = search_web(user_input)
        # Show search results to user in a separate message
        with st.chat_message("assistant"):
            st.markdown(search_result)
            print("✓ Search results displayed")
    except Exception as e:
        error_msg = f"Could not fetch latest info: {str(e)}"
        st.warning(error_msg)
        print(f"✗ {error_msg}")
        search_result = None
    
    # Build the message for AI with all available context
    full_message = user_input
    if search_result and search_result != "":
        full_message += f"\n\nLatest web search results:\n{search_result}"
    if weather_info:
        full_message += f"\n\nWeather info: {weather_info}"
    
    # Send to AI for response
    st.session_state.messages.append({"role": "user", "content": full_message})
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        with st.chat_message("assistant"):
            st.write(reply)
        print("✓ AI response generated")
    except Exception as e:
        error_msg = f"AI error: {str(e)}"
        st.error(error_msg)
        print(f"✗ {error_msg}")