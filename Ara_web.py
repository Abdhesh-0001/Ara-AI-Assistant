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
    """Search the web using a simple method"""
    try:
        # Try using requests to get search results
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&max_results=5"
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            results_text = f"🔍 **Search Results for '{query}':**\n\n"
            
            # Get results from RelatedTopics
            if 'RelatedTopics' in data and data['RelatedTopics']:
                for i, result in enumerate(data['RelatedTopics'][:3], 1):
                    if 'Text' in result:
                        results_text += f"**{i}. {result.get('FirstURL', 'Source')[:50]}**\n"
                        results_text += f"{result['Text'][:200]}...\n\n"
                
                return results_text
            else:
                return "Found search page but no detailed results."
        else:
            return "Could not connect to search service."
            
    except requests.Timeout:
        return "Search timed out - try a simpler query."
    except Exception as e:
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
        city = user_input.lower().replace("weather", "").replace("in", "").replace("of", "").strip()
        city = city if city else "London"
        reply = get_weather(city) + " 🌤️"
    # Search keywords that trigger web search
    search_keywords = ["news", "current", "latest", "today", "recent", "2024", "2025", "cm", "what happened", "covid", "election", "update"]

    # Only search if user asks for current/recent info
    if any(keyword in user_input.lower() for keyword in search_keywords):
        search_result = search_web(user_input)
        full_message = f"""
    User question: {user_input}

    Latest web search results:
    {search_result}

    Answer using the latest web information provided above.
    """
    else:
        full_message = user_input
        search_result = None

    if "weather" in user_input.lower():
        city = user_input.lower().replace("weather", "").replace("in", "").replace("of", "").strip()
        city = city if city else "London"
        reply = get_weather(city) + " 🌤️"
    else:
        st.session_state.messages.append({"role": "user", "content": full_message})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)