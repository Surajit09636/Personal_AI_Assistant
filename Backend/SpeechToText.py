from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os 
import mtranslate as mt 
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

# Get the InputLanguage setting from the environment variable 
InputLanguage = env_vars.get("InputLanguage")

# Define the HTML code for the speech recognition interface
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with the input language from the environmental variable
HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Write the modified HTML code to a file 
with open(r"Data/Voice.html", "w") as f:
    f.write(HtmlCode)
    
# Get the current working directory
current_dir = os.getcwd()
# Generate the file path for the HTML file
Link = f"{current_dir}/Data/Voice.html"

# Set Chrome options for the WebDriver
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

# Initialize the Chrome WebDriver using the ChromeDriver manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the path for the temporary file 
TempDirPath = rf"{current_dir}/Frontend/Files"

# Function to set the assistant's status by writing it to a file 
def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)
        
def QueryModifier(Query):
    new_Query = Query.lower().strip()
    Query_words = new_Query.split()
    Questions_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's", "can you"]
    
    # Check if the query is a question and add a question mark if necessary
    if any(word + " " in new_Query for word in Questions_words):
        if Query_words[-1][-1] in ['.', '?', '!']:
            new_Query = new_Query[:-1] + "?"
        else:
            new_Query += "?"
    else:
        # Add a period if the query is not a question
        if Query_words[-1][-1] not in ['.', '?', '!']:
            new_Query += "."
    
    return new_Query.capitalize()

# Function to perform speech recognition using WebDriver
def SpeechRecognition():
    # Open the HTML file in the browser
    driver.get("file:///" + Link)
    # Start speech recognition by clicking the start button
    driver.find_element(By.ID, "start").click()
    
    while True:
        try:
            # Get the recognition text from the HTML output element
            Text = driver.find_element(By.ID, "output").text
            
            # If the input language is English, return the modified query
            if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                return QueryModifier(Text)
            else:
                # If the input language is not English, translate the text and return it
                SetAssistantStatus("Translating...")
                return QueryModifier(mt.translate(Text, "en"))
            
        except Exception as e:
            pass
        
# Main execution block
if __name__ == "__main__":
    while True:
        # Continuously perform speech recognition and print the recognized text
        Text = SpeechRecognition()
        print(Text)
