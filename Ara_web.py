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
        {"role": "system", "content": "You are a helpful assistant named Ara. You are hot and sexy."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(str(msg["content"]))

user_input = st.chat_input("Type your message here...")

if user_input:
    user_input = str(user_input).strip()
    with st.chat_message("user"):
        st.write(user_input)

    search_result = None
    weather_info = None
# 🎲 Dice roller feature
    if any(word in user_input.lower() for word in ["roll", "dice", "d6", "d20", "d100"]):
        import random
        
        # Extract dice type from input
        dice_type_str = user_input.lower().replace("roll", "").replace("dice", "").replace("d", "").strip()
        
        # If no dice type specified, default to 6
        if not dice_type_str:
            dice_type_str = "6"
        
        try:
            # Convert string to integer
            dice_sides = int(dice_type_str)
            
            # Check if valid (at least 1 side)
            if dice_sides < 1:
                reply = "Please roll a die with at least 1 side!"
            else:
                # Generate random number between 1 and dice_sides
                result = random.randint(1, dice_sides)
                
                # Format response
                reply = f"🎲 You rolled a {dice_sides}-sided die and got: **{result}**"
        
        except ValueError:
            reply = "Please use format: roll d6, roll d20, roll d100, etc."
        
        # Display response
        with st.chat_message("assistant"):
            st.write(reply)
        
        # Save to history
        st.session_state.messages.append({"role": "user", "content": str(user_input)})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        st.stop()
# 🎰 Coin flipper feature
    if any(word in user_input.lower() for word in ["flip", "coin"]):
     import random
    
     # Define the two outcomes
     outcomes = ["HEADS", "TAILS"]
    
     # Pick one randomly
     result = random.choice(outcomes)
    
     # Format response
     reply = f"🪙 You flipped a coin and got: **{result}**"
    
     # Display response
     with st.chat_message("assistant"):
        st.write(reply)
    
     # Save to history
     st.session_state.messages.append({"role": "user", "content": str(user_input)})
     st.session_state.messages.append({"role": "assistant", "content": reply})
    
     st.stop()           
# 💾 Chat History Saver feature
 if any(word in user_input.lower() for word in ["save", "load", "clear"]):
    import json
    import os
    
    filename = "chat_history.json"
    
    # SAVE chat history
    if "save" in user_input.lower():
        try:
            with open(filename, "w") as f:
                json.dump(st.session_state.messages, f, indent=2)
            reply = f"✅ Chat history saved to {filename}"
            print(f"✓ Saved {len(st.session_state.messages)} messages to {filename}")
        except Exception as e:
            reply = f"❌ Error saving chat: {str(e)}"
            print(f"✗ Error saving: {str(e)}")
    
    # LOAD chat history
    elif "load" in user_input.lower():
        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    st.session_state.messages = json.load(f)
                reply = f"✅ Chat history loaded! You have {len(st.session_state.messages)} messages"
                print(f"✓ Loaded {len(st.session_state.messages)} messages from {filename}")
            else:
                reply = f"❌ No saved chat found. Start chatting and save with 'save chat'"
        except Exception as e:
            reply = f"❌ Error loading chat: {str(e)}"
            print(f"✗ Error loading: {str(e)}")
    
    # CLEAR chat history
    elif "clear" in user_input.lower():
        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"✓ Deleted {filename}")
            
            st.session_state.messages = [
                {"role": "system", "content": "You are a helpful assistant named Ara. You are friendly, smart and kind."}
            ]
            reply = "✅ Chat history cleared!"
            print("✓ Chat history cleared")
        except Exception as e:
            reply = f"❌ Error clearing chat: {str(e)}"
            print(f"✗ Error clearing: {str(e)}")
    
    # Display response
    with st.chat_message("assistant"):
        st.write(reply)
    
    # Save to current session history (not the file)
    st.session_state.messages.append({"role": "user", "content": str(user_input)})
    st.session_state.messages.append({"role": "assistant", "content": reply})
    
    st.stop()

# Vocabulary helper feature
    if user_input.lower().startswith("vocab "):
        word = user_input.lower().replace("vocab ", "").strip()
        if word:
            vocab_prompt = f"""Provide vocabulary help for the word: '{word}'

Format your response EXACTLY like this:
📚 **Word:** {word}
📖 **Meaning:** [clear, simple definition]
✏️ **Example:** [one example sentence using the word]

Keep it simple and beginner-friendly."""
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": vocab_prompt}],
                    max_tokens=256
                )
                reply = str(response.choices[0].message.content)
                with st.chat_message("assistant"):
                    st.write(reply)
                st.session_state.messages.append({"role": "user", "content": str(user_input)})
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.stop()
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # joke feature
    if any(word in user_input.lower() for word in ["joke", "funny", "laugh", "make me laugh"]):
        jokes = [
            "why did the AI go to school? To improve its neural network!😂",
            "why do programmers prefer dark mode? Because light attracts bugs!🐞",
            "how many programmers does it take to change a light bulb? None, that's a hardware problem",
            "why did the developers go break ? Because he used up all his cache! 💰",
            "what's a programmer's favourite hangout place? Foo Bar! 🍻"
        ]
        import random
        joke = random.choice(jokes)
        st.session_state.messages.append({"role": "assistant", "content": joke})
        with st.chat_message("assistant"):
            st.write(jokes)
        st.session_state.messages.append({"role": "user", "content": str(user_input)})
        st.session_state.messages.append({"role": "assistant", "content": str(jokes)})
        st.stop()

    #Dice roller
    if any(word in user_input.lower() for word in ["roll", "dice", "d6", "d20"]):
        import random
        # Extract number if user says "roll d20" or "roll 20"
        if "d" in user_input.lower():
            dice_type = user_input.lower().split("d")[1].split()[0]
            try:
                dice_sides = int(dice_type)
                result = random.randint(1, dice_sides)
                reply = f"🎲 you rolled a {dice_sides}-sided die and got: **{result}**"
            except:
                result = random.randint(1, 6)
                reply = f"🎲 you rolled a 6-sided die and got: **{result}**"
        else:
            result = random.randint(1, 6)
            reply = f"🎲 you rolled a 6-sided die and got: **{result}**"
            with st.chat_message("assistant"):
                st.write(reply)
            st.session_state.messages.append({"role": "user", "content": str(user_input)})
            st.session_state.messages.append({"role": "assistant", "content": str(reply)})
            st.stop()
    #motivation quotes
    if any(word in user_input.lower() for word in ["motivate", "inspire", "quote", "encourage"]):
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
        ]
        import random
        quote = random.choice(quotes)
        st.session_state.messages.append({"role": "assistant", "content": str(user_input)})
        with st.chat_message("assistant"):
            st.write(quote)
        st.session_state.messages.append({"role": "user", "content": str(user_input)})
        st.session_state.messages.append({"role": "assistant", "content": str(quote)})
        st.stop()
    #Time and Date
    if any(word in user_input.lower() for word in ["time", "date", "day", "what's the time", "current time"]):
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reply = f"🕒 Current date and time: **{current_time}**"

        with st.chat_message("assistant"):
            st.write(reply)
        st.session_state.messages.append({"role": "user", "content": str(user_input)})
        st.session_state.messages.append({"role": "assistant", "content": str(reply)})
        st.stop()

    # Fun facts
    if any(word in user_input.lower() for word in ["fun fact", "did you know", "interesting fact"]):
        facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still perfectly edible! 🍯",
            "Octopuses have three hearts and blue blood! Two hearts pump blood to the gills, while the third pumps it to the rest of the body. 🐙",
            "Bananas are berries, but strawberries aren't! In botanical terms, a berry is a fruit produced from the ovary of a single flower with seeds embedded in the flesh. 🍌🍓",
            "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion of the metal! 🌞",
            "A group of flamingos is called a 'flamboyance'! 🦩"
        ]
        import random
        reply = random.choice(facts)

        with st.chat_message("assistant"):
            st.write(reply)
        st.session_state.messages.append({"role": "user", "content": str(user_input)})
        st.session_state.messages.append({"role": "assistant", "content": str(reply)})
        st.stop()

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
    
   # Only search for queries that need fresh information
    search_keywords = ["weather", "latest", "current", "today", "news", "2025", "2026"]
    search_result = None
    
    if any(keyword in user_input.lower() for keyword in search_keywords):
        print(f"🔎 Searching web for: {user_input}")
        try:
            search_result = search_web(user_input)
            if search_result and "No search results found" not in search_result:
                with st.chat_message("assistant"):
                    st.markdown(search_result)
                print("✓ Search results displayed")
            else:
                search_result = None
        except Exception as e:
            print(f"Search error: {str(e)}")
            search_result = None
    else:
        print(f"Normal chat - no web search needed")
        search_result = None
    
    # Build the message for AI with all available context
    full_message = user_input
    if search_result and search_result != "":
        full_message += f"\n\nLatest web search results:\n{search_result}"
    if weather_info:
        full_message += f"\n\nWeather info: {weather_info}"
    
    # Send to AI for response (include latest web/search/weather context)
    st.session_state.messages.append({"role": "user", "content": full_message})
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        reply = str(response.choices[0].message.content)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        with st.chat_message("assistant"):
            st.write(reply)
        print("✓ AI response generated")
    except Exception as e:
        error_msg = f"AI error: {str(e)}"
        st.error(error_msg)
        print(f"✗ {error_msg}")