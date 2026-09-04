import streamlit as st
import requests
import os
from dotenv import load_dotenv
from groq import Groq
from duckduckgo_search import DDGS
# Add this RIGHT AFTER the imports section
# ===== RIDDLE GENERATOR CLASS =====

class RiddleGenerator:
    """A class to manage riddles"""
    
    def __init__(self):
        self.riddles = [
            {
                "question": "I have cities but no houses, forests but no trees, water but no fish. What am I?",
                "answer": "map"
            },
            {
                "question": "What can travel around the world while staying in a corner?",
                "answer": "stamp"
            },
            {
                "question": "The more you take, the more you leave behind. What am I?",
                "answer": "footsteps"
            },
            {
                "question": "What has a head and a tail but no body?",
                "answer": "coin"
            },
            {
                "question": "What can run but never walks, has a mouth but never talks, has a bed but never sleeps?",
                "answer": "river"
            },
            {
                "question": "I'm light as a feather, yet the strongest person can't hold me for five minutes. What am I?",
                "answer": "breath"
            }
        ]
        self.current_riddle = None
        self.guesses = 0
    
    def get_random_riddle(self):
        """Returns a random riddle"""
        import random
        self.current_riddle = random.choice(self.riddles)
        self.guesses = 0
        return self.current_riddle
    
    def check_answer(self, user_answer):
        """Check if user's answer is correct"""
        if not self.current_riddle:
            return "Please ask for a riddle first!"
        
        self.guesses += 1
        correct_answer = self.current_riddle["answer"].lower()
        user_answer_clean = user_answer.lower().strip()
        
        if user_answer_clean == correct_answer:
            return f"✅ Correct! The answer is: **{self.current_riddle['answer']}**"
        else:
            return f"❌ Wrong! Try again. (Attempt {self.guesses})"
    
    def add_riddle(self, question, answer):
        """Add a new riddle"""
        new_riddle = {
            "question": question,
            "answer": answer
        }
        self.riddles.append(new_riddle)
        return f"✅ Riddle added! Now I have {len(self.riddles)} riddles"

# Create global riddle generator object
riddle_gen = RiddleGenerator()

# ===== END RIDDLE GENERATOR CLASS =====

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# ===== JOKE GENERATOR CLASS =====

class JokeGenerator:
    """A class to manage jokes"""
    
    def __init__(self):
        self.jokes = [
            "Why did the AI go to school? To improve its neural networks! 😂",
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
            "Why did the developer go broke? Because he used up all his cache! 💰",
            "What's a programmer's favorite hangout place? Foo Bar! 🍺",
            "Why do Java developers wear glasses? Because they don't C#! 👓",
            "How many programmers does it take to change a light bulb? None, that's a DevOps problem! 🔦",
            "Why did the programmer quit his job? Because he didn't get arrays! 📚"
        ]
        self.jokes_told = 0
    
    def tell_joke(self):
        """Returns a random joke"""
        import random
        self.jokes_told += 1
        return random.choice(self.jokes)
    
    def get_total_jokes(self):
        """Returns how many jokes are in the collection"""
        return len(self.jokes)
    
    def add_joke(self, new_joke):
        """Add a new joke"""
        self.jokes.append(new_joke)
        return f"✅ New joke added! Now I have {len(self.jokes)} jokes"

# Create global joke generator object
joke_gen = JokeGenerator()

# ===== END JOKE GENERATOR CLASS =====

# ===== QUIZ GAME CLASS =====

class QuizGame:
    """A class to manage quiz games"""
    
    def __init__(self):
        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["A) London", "B) Paris", "C) Berlin", "D) Madrid"],
                "correct": "B"
            },
            {
                "question": "What is 2 + 2?",
                "options": ["A) 3", "B) 4", "C) 5", "D) 6"],
                "correct": "A"
            },
            {
                "question": "What is the largest planet?",
                "options": ["A) Earth", "B) Mars", "C) Jupiter", "D) Saturn"],
                "correct": "C"
            },
            {
                "question": "What year did Python launch?",
                "options": ["A) 1989", "B) 1995", "C) 2000", "D) 2005"],
                "correct": "A"
            },
            {
                "question": "How many continents are there?",
                "options": ["A) 5", "B) 6", "C) 7", "D) 8"],
                "correct": "C"
            }
        ]
        self.current_question = None
        self.score = 0
        self.total_answered = 0

    def start_game(self):
        """Start a new game"""
        import random
        self.current_question = random.choice(self.questions)
        self.score = 0
        self.total_answered = 0
        
        question_text = self.current_question["question"]
        options_text = "\n".join(self.current_question["options"])
        return f"🎯 **Quiz Game Started!**\n\n{question_text}\n\n{options_text}\n\n(Type A, B, C, or D)"
    
    def check_answer(self, user_answer):
        """Check if answer is correct"""
        if not self.current_question:
            return "Please start a game first with 'quiz'!"
        
        user_answer = user_answer.upper().strip()
        
        if user_answer not in ["A", "B", "C", "D"]:
            return "❌ Please answer with A, B, C, or D!"
        
        self.total_answered += 1
        correct_answer = self.current_question["correct"]
        
        if user_answer == correct_answer:
            self.score += 1
            return f"✅ Correct! Your score: {self.score}/{self.total_answered}"
        else:
            return f"❌ Wrong! The correct answer is {correct_answer}. Your score: {self.score}/{self.total_answered}"
    
    def next_question(self):
        """Get the next question"""
        import random
        self.current_question = random.choice(self.questions)
        
        question_text = self.current_question["question"]
        options_text = "\n".join(self.current_question["options"])
        return f"🎯 **Next Question!**\n\n{question_text}\n\n{options_text}"
    
    def end_game(self):
        """End game and show final score"""
        if self.total_answered == 0:
            return "No questions answered yet!"
        
        percentage = (self.score / self.total_answered) * 100
        return f"🏆 **Game Over!**\n\nFinal Score: {self.score}/{self.total_answered} ({percentage:.0f}%)"

# Create global quiz game object
quiz_game = QuizGame()

# ===== END QUIZ GAME CLASS =====

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
            
            return response
        else:
            return "Live weather data is currently unavailable."
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
# 💾Chat History Saver Feature
    if any(word in user_input.lower() for word in ["save", "load", "clear"]):
        import json
        import os
        filename = "chat_history.json"

        # SAVE chat history
        if "save" in user_input.lower():
            try:
                with open (filename,"w") as f:
                    json.dump(st.session_state.messages, f , indent=0)
                reply = f"✅ Chat history saved to {filename}"
                st.write(f"✓ saved {len(st.session_state.messages)} messages to {filename}")
            except Exception as e:
                reply = f"❌ Error saving chat: {str(e)}"
                st.write(f"✗ Error saving: {str(e)}")

        # LOAD chat history
        elif "load" in user_input.lower():
            try:
                if os.path.exists(filename):
                    with open(filename, "r") as f:
                        st.session_state.messages = json.load(f)
                    
                    reply = f"✅Chat history loaded! You have {len(st.session_state.messages)} messages"
                    st.write(f"✓ loaded {len(st.session_state.messages)} messages from {filename}")
                else:
                    reply = f"❌ No saved chat found. start chatting and save with 'save chat'"
            except Exception as e:
                reply = f"❌ Error loading chat: {str(e)}"
                st.write(f"✗ Error loading: {str(e)}")

        # Clear Chat History
        elif "clear" in user_input.lower():
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"✓ Deleted {filename}")

                st.session_state.messages = [
                    {"role": "system", "content": "You are a helpful assistant named Ara. You are hot and sexy."}
                ]
                reply = "✅chat history cleared!"
                st.write(f"✓ Chat history cleared")
            except Exception as e:
                reply = f"❌ Error clearing chat: {str(e)}"
                st.write(f"✗ Error clearing: {str(e)}")

        # Display response
        with st.chat_message("assistant"):
            st.write(reply)

        # Save to current session history (not the file)
        st.session_state.messages.append({"role": "user", "content": str(user_input)})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.stop()

# 🧩 Riddle Generator feature
    if any(word in user_input.lower() for word in [
        "riddle",
        "give me a riddle",
        "ask me a riddle"
    ]):
        import random
        if any(word not in ["riddle", "give me a riddle", "ask me a riddle"] for word in user_input.lower().split()):
            reply = riddle_gen.check_answer(user_input)
        else:
            # User wants a new riddle
            riddle = riddle_gen.get_random_riddle()
            reply = f"🧩 **Riddle:** {riddle['question']}\n\n(Type your answer!)"
        
        # Display response
        with st.chat_message("assistant"):
            st.write(reply)
        
        # Save to history
        st.session_state.messages.append({"role": "user", "content": str(user_input)})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        st.stop()

# 🎯 Quiz Game feature
    if any(word in user_input.lower() for word in [
        "quiz",
        "play quiz",
        "start quiz"
    ]):
        if user_input.lower() == "what is 2+2":
            st.write("The answer is 3")
            st.stop()

        # Start new game
        reply = quiz_game.start_game()
        
        # Display response
        with st.chat_message("assistant"):
            st.write(reply)
        
        # Save to history
        st.session_state.messages.append({"role": "user", "content": str(user_input)})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        st.stop()
    
    # Quiz answer checking
    if quiz_game.current_question and any(char in user_input.upper() for char in ["A", "B", "C", "D"]):
        if len(user_input.strip()) == 1:  # Single character answer
            # User is answering the quiz
            reply = quiz_game.check_answer(user_input)
            
            # Ask if they want next question
            reply += "\n\n(Type 'next' for next question or 'end' to finish)"
            
            # Display response
            with st.chat_message("assistant"):
                st.write(reply)
            
            # Save to history
            st.session_state.messages.append({"role": "user", "content": str(user_input)})
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            st.stop()
    
    # Next question in quiz
    if quiz_game.current_question and user_input.lower() == "next":
        reply = quiz_game.next_question()
        
        # Display response
        with st.chat_message("assistant"):
            st.write(reply)
        
        # Save to history
        st.session_state.messages.append({"role": "user", "content": str(user_input)})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        st.stop()
    
    # End quiz
    if quiz_game.current_question and user_input.lower() == "end":
        reply = quiz_game.end_game()
        quiz_game.current_question = None  # Reset
        
        # Display response
        with st.chat_message("assistant"):
            st.write(reply)
        
        # Save to history
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
                    model="openai/gpt-oss-120b",
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

    # 😂 Joke feature (REFACTORED TO CLASS)
    if any(word in user_input.lower() for word in [
        "joke",
        "funny",
        "laugh",
        "make me laugh"
    ]):
        # Get joke from class
        reply = joke_gen.tell_joke()
        
        # Display response
        with st.chat_message("assistant"):
            st.write(reply)
        
        # Save to history
        st.session_state.messages.append({"role": "user", "content": str(user_input)})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
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
            st.write(f"Weather fetched: {city}")
        except Exception as e:
            st.write(f"Weather error: {str(e)}")
            weather_info = None
    
   # Only search for queries that need fresh information
    search_keywords = ["weather", "latest", "current", "today", "news", "2025", "2026"]
    search_result = None
    
    if any(keyword in user_input.lower() for keyword in search_keywords):
        st.write(f"🔎 Searching web for: {user_input}")
        try:
            search_result = search_web(user_input)
            if search_result and "No search results found" not in search_result:
                with st.chat_message("assistant"):
                    st.markdown(search_result)
                st.write("✓ Search results displayed")
            else:
                search_result = None
        except Exception as e:
            st.write(f"Search error: {str(e)}")
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
            model="openai/gpt-oss-120b",
            messages=st.session_state.messages
        )
        max_tokens = 180
        max_temperature = 0.2
        reply = str(response.choices[0].message.content)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        with st.chat_message("assistant"):
            st.write(reply)
        st.write("✓ AI response generated")
    except Exception as e:
        error_msg = f"AI error: {str(e)}"
        st.error(error_msg)
        st.write(f"✗ {error_msg}")