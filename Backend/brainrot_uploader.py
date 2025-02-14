
from dotenv import load_dotenv
import os
from time import sleep
import google.generativeai as genai
from youtube import my_upload_video
# Load environment variables
load_dotenv("../.env")
count = 0


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

import requests
import json

def generate_video(video_subject, ai_model, voice, paragraph_number, youtube_upload, use_music, zip_url, threads, subtitles_position, custom_prompt, color):
    global count
    print("Generating video...")

    # Construct data to be sent to the server
    data = {
        "videoSubject": video_subject,
        "aiModel": ai_model,
        "voice": voice,
        "paragraphNumber": paragraph_number,
        "automateYoutubeUpload": youtube_upload,
        "useMusic": use_music,
        "zipUrl": zip_url,
        "threads": threads,
        "subtitlesPosition": subtitles_position,
        "customPrompt": custom_prompt,
        "color": color,
    }
    url = "http://localhost:8081/api/generate"
    
    try:
        print("killing old chrome windows")
        os.system("pkill --oldest chrome")
        
        # Send the actual request to the server
        response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json", "Accept": "application/json"})
        response_data = response.json()
        print(response_data)
        
        res = response_data.get("message", "No message received")
        print(res)
        if res.startswith("Video generated"):
            count +=1
            print("Video generated since program is running: ",count)
            return True
        else:
            return False
            
    except Exception as error:
        print("An error occurred. Please try again later.")
        print(error)
        return False

def generate_subject_and_prompt_gemini():
    model = genai.GenerativeModel('gemini-pro')
    prompt ="""
    generate a subject about anything. The subject MUST BE A SINGLE WORD or a well known curiosity.
    
    Output example:

    what is <subject>
    who is <subject>

    (replace <subject> with the generated subject)
    """
    response_model = model.generate_content(prompt)
    response = response_model.text
    print(response)
    return response

print ('Listening ...')
import json
import time

# File path to the JSON file
file_path = "persistent.json"

# Load existing JSON data from file
def load_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"subjects": []}  # Default structure if file doesn't exist

# Save JSON data to file
def save_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Add a subject to the list
def add_subject(subject):
    data = load_json(file_path)
    data["subjects"].append(subject)
    save_json(file_path, data)

from datetime import date
from datetime import datetime as dt


current_hour = dt.now().hour
current_day = date.today().strftime("%Y-%m-%d")
print("--------BRAINROT UPLOADER STARTED--------")
print("Current day:", current_day)
print("Current hour:",current_hour)
cooldown_sec = 115200 # 32h (I suggest to upload 1 video per day with 32h shifts)
#cooldown_sec = 60*10 # 10min
while 1:
    while(1): # loop until generate 1 video on new subject
        try:
            sub = generate_subject_and_prompt_gemini()
        except Exception as e:
            print(f"fail to generate subject: {e}")
            print("retry in 5 seconds")
            sleep(5)
            continue
        subjects = load_json(file_path)["subjects"]
        clean_sub = sub.replace(' ','').upper()
        if clean_sub in subjects:
            print("subject already used.. trying again")
        else:
            add_subject(clean_sub)
            print("new subject added to persistent.json")
            print(f"generating {sub} ")
            prompt_to_use = '../prompt.txt'
            with open(prompt_to_use,'r',  encoding='utf-8', errors='ignore') as file:
                prompt = file.read()
            yt_upload = True
            success = generate_video(sub, "gemmini", "en_male_funny", 1, yt_upload, False, "", 2, "center,center", prompt, "#FFFF00")
            if success:
                print("successfully generated")
                break
            else:
                print("fail repeat")
        print("retry in 5 seconds")
        time.sleep(5)
    print(f"COOLING DOWN.. WAITING {cooldown_sec}s")
    time.sleep(cooldown_sec) # cooldown 