from groq import Groq # Importing the Groq library to use its API
from json import load, dump # Importing functions to read and write json files
import datetime #Importing the date-time module for date and time information
from dotenv import dotenv_values # Importing dotenv_values to read environment variables from a .env file

# Load environment variables from the .env file 
env_vars = dotenv_values(".env")

# Retrive specific environment variables to username, assistant name, and API key
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPTKey")

#Initialize the Groq clint using the provided API key
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages 
messages = []

# Define a system message thet provides a contxt to the AI chatbot about it's role and behaviour
system = """"""

# A list of system instructions for the chatbot 
SyetemChatBot = [
    {"role": "system", "content": System}
]

# Attempt to load the chat log from a Json file 
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f) #load existing messages from the chat log
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Function to get real time date and time inforation
def RealTimeInformation():
    current_date_time = datetime.datetime.now() #get the current date time 
    day = current_date_time.strftime("%A") # Day of the week
    