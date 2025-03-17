from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt # Import from google search and youtube playback 
from dotenv import dotenv_values 
from bs4 import BeautifulSoup # Import BeautifilSoup for praising HTML content 
from rich import print # Import rich for styled console output
from groq import Groq
import webbrowser # For opening urls
import subprocess # Import subprocess for interacting with system
import requests
import keyboard # For keyboard related actions
import asyncio
import os

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Define CSS classes for praising specific elements in HTML content
classes = [
    "zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTKOO", "vlzY6d",
    "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making a web request
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) chrome/100.04896.75 safari/537.36'

client = Groq(api_key=GroqAPIKey)

# Professional response for user interaction
professional_responses = [
    "Your satisfaction is my top priority; fell free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask"
]

# List to store AI's messages
messages = []

# System message to provide context to the AI
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. you have to write content like writing, script writing"}]

# Func to to google search
def GoogleSearch(Topic):
    search(Topic)
    return True


# function to generate content using ai and save it to a file 
def Content(Topic):

    
    # Nested func to open a file in notepad
    def OpenNotepad(File):
        default_text_editor = 'Notepad.exe'
        subprocess.Popen([default_text_editor, File])
        
        def ContentWriterAI(prompt):
            messages.append({"role": "user", "content": f"{prompt}"})
            
            completion = client.chat.completions.create(
                model = "mixtral-8×7b-32768",
                messages = SystemChatBot + messages,
                max_tokens = 2048,
                temperature = 0.7,
                top_p = 1,
                stream = True,
                stop=None
            )
            
            Answer = ""
            
            for chunk in completion:
                if chunk.choises[0].delta.content: # check if the content is in the current chunck
                    Answer += chunk.choises[0].delta.content # Append the content to the answer
                    
            Answer = Answer.replace("</s>", "")
            messages.append({"role": "assistant", "content": Answer})
            return Answer
        
        Topic: str = Topic.replace("Content", "")
        ContentByAI = ContentWriterAI(Topic) # Generate content using AI 
        
        # Save the generated content to a text file 
        with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
            file.write(ContentByAI)
            file.close()
            
        OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt") # Open the file in notepad
        return True
    

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" # Construct youtube search query
    webbrowser.open(Url4Search) # Open the constructed url in the default browser
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return[]
            soup = BeautifulSoup(html, 'html.parser') # parse the html content
            links = soup.find_all('a', {'jsname': 'UWckNb'}) # Find relevant links
            return [link.get('herf') for link in links] #return the links
        
        # Nested function for google search and retrive HTML
        def search_google(query):
            url = f"https://www.google.com/search?q={query}" # Construct
            headers = {'User-Agent': useragent} # use the predefined user-agent
            response = sess.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.text # Return the HTML content
            else:
                print("Failed to retrive search results.") # Print an error message 
            return None
        
        html = search_google(app) # perform the google search
        
        if html:
            link = extract_links(html)[0] #Extract the first link from the search result
            webopen(link) # Open the link in a webbrowser 
            
        return True
    
#function to close the application
def CloseApp(app):
    
    if "chrome" in app:
        pass # Skip if the app is chrome
    else:
        try:
            close(app, match_closest=True, output=True, throw_error= True) # Attempt to close the app
            return True #b Indicate success
        except:
            return False
        
def System(command):
    def mute():
        keyboard.press_and_release("volume_mute") # simulate the mute key press
        
    def unmute():
        keyboard.press_and_release("volume_unmute") 
        
    def volume_up():
        keyboard.press_and_release("volume_up")
        
    def volume_down():
        keyboard.press_and_release("volume_down") 
        
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume_down":
        volume_down()
        
    return True # Indicate success

async def TranslateAndExecute(commands: list[str]):
    funcs =[]
    for command in commands:
        if command.startswith("open"):
            if "open it " in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("close ")) # Scheduling app opening
                funcs.append(fun)
                
        elif command.startswith("general "): # placeholder for general command
            pass
        elif command.startswith("realtime "): # placeholder for real time command
            pass
        elif command.startswith("closel "): # Handel close command 
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close ")) # Schedule app closing
            funcs.append(fun)
            
        elif command.startswith("play "): # handel play command 
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play ")) # Schedule music playing
            funcs.append(fun)
            
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
            
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")) # Schedule google
            funcs.append(fun)
            
        elif command.startswith("Youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("Youtube search ")) # Schedule youtube
            funcs.append(fun)
            
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system ")) # Schedule system command
            funcs.append(fun)
            
        else:
            print(f"No function found for {command}")
            
    results = await asyncio.gather(*funcs)
    
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result
            
async def Automation(commands: list[str]):
    
    async for result in TranslateAndExecute(commands):
        pass
    return True