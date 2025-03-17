from googlesearch import search
from groq import Groq  # Importing Groq library to use its API
from json import load, dump  # Importing functions to read and write JSON files
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")

# Retrieve values from .env
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")  

# Ensure API Key is set
if not GroqAPIKey:
    raise ValueError("Error: GroqAPIKey is missing. Check your .env file and ensure it's correctly loaded.")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# System instructions for chatbot
System = f"""Hello, I am {Username}. You are a very accurate and advanced AI named {Assistantname} with real-time up-to-date information.
*** Provide Answers In a Professional Way, using full stops, commas, question marks, and proper grammar. ***
*** Just answer the question from the provided data in a professional way. ***"""

# Load chat history or create an empty one if file doesn't exist
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
    messages = []

# ✅ Fixed `num_resukts` typo
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

    Answer += "[end]"
    return Answer

# Removes empty lines from the answer
def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

# Initial chatbot context
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Get real-time date and time
def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    return (
        f"Use this real-time information if needed:\n"
        f"Day: {day}\n"
        f"Date: {date}\n"
        f"Month: {month}\n"
        f"Year: {year}\n"
        f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    )

# Real-time search and AI response function
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages  # ✅ Fixed `SyatemChatBot` typo

    # Load chat history
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)

    messages.append({"role": "user", "content": prompt})
    
    # Perform Google Search
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Call AI model
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    
    for chunk in completion:
        if chunk.choices[0].delta.content:  
            Answer += chunk.choices[0].delta.content 
                
    Answer = Answer.strip().replace("</s>", "")  
    messages.append({"role": "assistant", "content": Answer})

    # Save chat history
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    # Remove last system message
    SystemChatBot.pop()
    
    return AnswerModifier(Answer)

# CLI interaction
if __name__ == "__main__":
    while True:
        prompt = input("Enter your Query: ")
        print(RealtimeSearchEngine(prompt))
