import os
from utils import *
from dotenv import load_dotenv
import random
from youtube import simple_upload_video
import shutil
from time import sleep

# Load environment variables
load_dotenv("../.env")
# Check if all required environment variables are set
# This must happen before importing video which uses API keys without checking
check_env_vars()

from gpt import *
from video import *

from uuid import uuid4
from tiktokvoice import *
from flask_cors import CORS
from termcolor import colored
from apiclient.errors import HttpError
from flask import Flask, request, jsonify
from moviepy.config import change_settings



# Set environment variables
SESSION_ID = os.getenv("TIKTOK_SESSION_ID")
openai_api_key = os.getenv('OPENAI_API_KEY')
change_settings({"IMAGEMAGICK_BINARY": os.getenv("IMAGEMAGICK_BINARY")})

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Constants
HOST = "0.0.0.0"
PORT = 8081
GENERATING = False


# Generation Endpoint
@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        # Set global variable
        global GENERATING
        GENERATING = True

        # Clean
        clean_dir("../temp/")
        clean_dir("../subtitles/")


        # Parse JSON
        data = request.get_json()
        paragraph_number = int(data.get('paragraphNumber', 1))  # Default to 1 if not provided
        
        ai_model = data.get('aiModel')  # Get the AI model selected by the user
        
        n_threads = data.get('threads')  # Amount of threads to use for video generation
        
        
        subtitles_position = data.get('subtitlesPosition')  # Position of the subtitles in the video
        
        text_color = data.get('color') # Color of subtitle text
        

        # Get 'useMusic' from the request data and default to False if not provided
        use_music = data.get('useMusic', False)

        # Get 'automateYoutubeUpload' from the request data and default to False if not provided
        automate_youtube_upload = data.get('automateYoutubeUpload', False)

        # Get the ZIP Url of the songs
        songs_zip_url = data.get('zipUrl')

        

        # Print little information about the video which is to be generated
        print(colored("[Video to be generated]", "blue"))
        print(colored("   Subject: " + data["videoSubject"], "blue"))
        print(colored("   AI Model: " + ai_model, "blue"))  # Print the AI model being used
        print(colored("   Custom Prompt: " + data["customPrompt"], "blue"))  # Print the AI model being used



        if not GENERATING:
            return jsonify(
                {
                    "status": "error",
                    "message": "Video generation was cancelled.",
                    "data": [],
                }
            )
        
        voice = data["voice"]
        voice_prefix = voice[:2]
        
        
        
        if not voice:
            print(colored("[!] No voice was selected. Defaulting to \"en_male_funny\"", "yellow"))
            voice = "en_male_funny"
            voice_prefix = voice[:2]

        
        print(colored("loading prompt.txt","red"))
        with open('../prompt.txt','r',  encoding='utf-8', errors='ignore') as file:
            prompt = file.read()
        # Generate a script
        script = generate_script(data["videoSubject"], paragraph_number, ai_model, voice,prompt )  # Pass the AI model to the script generation

        

        # Let user know
        print(colored("[+] Script generated!\n", "green"))

        if not GENERATING:
            return jsonify(
                {
                    "status": "error",
                    "message": "Video generation was cancelled.",
                    "data": [],
                }
            )

        # Split script into sentences
        sentences = script.split(". ")

        # Remove empty strings
        sentences = list(filter(lambda x: x != "", sentences))
        paths = []

        # Generate TTS for every sentence
        for sentence in sentences:
            if not GENERATING:
                return jsonify(
                    {
                        "status": "error",
                        "message": "Video generation was cancelled.",
                        "data": [],
                    }
                )
            current_tts_path = f"../temp/{uuid4()}.mp3"
            tts(sentence, voice, filename=current_tts_path)
            audio_clip = AudioFileClip(current_tts_path)
            paths.append(audio_clip)

        # Combine all TTS files using moviepy
        final_audio = concatenate_audioclips(paths)
        tts_path = f"../temp/{uuid4()}.mp3"
        final_audio.write_audiofile(tts_path)

        try:
            subtitles_path = generate_subtitles(audio_path=tts_path, sentences=sentences, audio_clips=paths, voice=voice_prefix)
        except Exception as e:
            print(colored(f"[-] Error generating subtitles: {e}", "red"))
            subtitles_path = None

        # Concatenate videos
        temp_audio = AudioFileClip(tts_path)
         
        directory_path = '../backgrounds'

        # List all files in the directory
        bgs = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        # Pick a random file
        random_bg = f"../backgrounds/{random.choice(bgs)}"
        print("choose random bg: ",random_bg)
        full_len_video = VideoFileClip(random_bg)
        bg_video = "../temp/trimmed.mp4"
        trimmed = full_len_video.subclip(0, temp_audio.duration)
        
        trimmed.write_videofile(bg_video,fps=30,codec="libx264", audio_codec="aac" )
        # Put everything together
        try:
            final_video_path = generate_video(bg_video, tts_path, subtitles_path, n_threads or 2, subtitles_position, text_color or "#FFFF00" )
        except Exception as e:
            print(colored(f"[-] Error generating final video: {e}", "red"))
            final_video_path = None

        # Define metadata for the video, we will display this to the user, and use it for the YouTube upload
        title, description, keywords = generate_metadata(data["videoSubject"], script, ai_model)
        subject = data["videoSubject"]
        title = f"{subject}? SKIBIDI QUIZ 🚽🤯"
        print(colored("[-] Metadata for upload:", "blue"))
        print(colored("   Title: ", "blue"))
        print(colored(f"   {title}", "blue"))
        print(colored("   Description: ", "blue"))
        print(colored(f"   {description}", "blue"))
        print(colored("   Keywords: ", "blue"))
        #print(colored(f"  {', '.join(keywords)}", "blue"))
        short_hash = "#memes #meme #brainrot #funnymemes #shorts"
        short_tags = f"memes,brainrot,funny,meme,{subject}"
        print(colored(short_tags, "blue"))
        if automate_youtube_upload:
            # Start Youtube Uploader
            # Check if the CLIENT_SECRETS_FILE exists
            client_secrets_file = os.path.abspath("./client_secret.json")
            SKIP_YT_UPLOAD = False
            if not os.path.exists(client_secrets_file):
                SKIP_YT_UPLOAD = True
                print(colored("[-] Client secrets file missing. YouTube upload will be skipped.", "yellow"))
                print(colored("[-] Please download the client_secret.json from Google Cloud Platform and store this inside the /Backend directory.", "red"))

            # Only proceed with YouTube upload if the toggle is True  and client_secret.json exists.
            if not SKIP_YT_UPLOAD:
                # Choose the appropriate category ID for your videos
                video_category_id = "24"  # Entertainment
                privacyStatus = "public"  # "public", "private", "unlisted"
                
                yt_title = title 
                yt_title = yt_title[:99]
                yt_desc = description + " "+short_hash
                video_metadata = {
                    'video_path': os.path.abspath(f"../temp/{final_video_path}"),
                    'title': yt_title,
                    'description': yt_desc,
                    'category': video_category_id,
                    'keywords': ",".join(keywords),
                    'privacyStatus': privacyStatus,
                }

                # Upload the video to YouTube
                try:
                    # Unpack the video_metadata dictionary into individual arguments
                    video_response = simple_upload_video(
                        video_path=video_metadata['video_path'],
                        title=video_metadata['title'],
                        description=video_metadata['description'],
                        category=video_metadata['category'],
                        keywords=video_metadata['keywords'],
                        privacy_status=video_metadata['privacyStatus']
                    )
                    print("Uploaded video!!")
                except HttpError as e:
                    print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

        video_clip = VideoFileClip(f"../temp/{final_video_path}")
        
        shutil.copy(f"../temp/{final_video_path}", f"../{final_video_path}")
        


        # Let user know
        print(colored(f"[+] Video generated: {final_video_path}!", "green"))
        
        # Stop FFMPEG processes
        if os.name == "nt":
            # Windows
            os.system("taskkill /f /im ffmpeg.exe")
        else:
            # Other OS
            os.system("pkill -f ffmpeg")

        GENERATING = False

        # Return JSON
        return jsonify(
            {
                "status": "success",
                "message": "Video generated! See MoneyPrinter/output.mp4 for result.",
                "data": final_video_path,
            }
        )
    except Exception as err:
        print(colored(f"[-] Error: {str(err)}", "red"))
        return jsonify(
            {
                "status": "error",
                "message": f"Could not retrieve stock videos: {str(err)}",
                "data": [],
            }
        )


@app.route("/api/cancel", methods=["POST"])
def cancel():
    print(colored("[!] Received cancellation request...", "yellow"))

    global GENERATING
    GENERATING = False

    return jsonify({"status": "success", "message": "Cancelled video generation."})


if __name__ == "__main__":

    # Run Flask App
    app.run(debug=True, host=HOST, port=PORT)
