import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

def open_images(prompt):
    folder_path = r"Data" # folder where the image are stored
    prompt = prompt.replace(" ", "_") # Replaces spaces in prompt with unerscore
    
    # Genereate the file name for the images
    Files = [f"{prompt}{i}.jpg" for i in range(1,5)]
    
    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        
        try:
            # Try to open and display the image
            img = Image.open(image_path)
            print("opening image: {image_path}")
            img.show()
            sleep(1) # Pause for 1 sec before showing the next image
            
        except IOError:
            print(f"Unable to open{image_path}")
 
 # API details for the huggingface stable diffsion model           
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# Async function to send the query to the hugging face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Async function to generate images based on the given prompt
async def generate_image(prompt: str):
    tasks = []
    
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)
    
    # wait for all tasks for complete
    image_bytes_list = await asyncio.gather(*tasks)
    
    # Save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        with open (fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
            f.write(image_bytes)
            
# wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_image(prompt)) # Run the async image generation
    open_images(prompt) # Open the generate images
    
# Main loop to monitor for image generation requests
while True:
    
    try:
        # Read the status and prompt from the date file
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()
            
        Prompt, Status = Data.split(",")
        
        # If the status indicates an image generation request
        if Status == "True":
            print("Generating images....")
            ImageStatus = GenerateImages(prompt=Prompt)
            
            # Reset the status in the file after generating image
            with open (r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
                break
            
        else:
            sleep(1) # Wait for 1 second before checking again
        
    except:
        pass