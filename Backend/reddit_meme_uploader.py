import os
from utils import *
from dotenv import load_dotenv

from youtube import simple_upload_video

# Load environment variables
load_dotenv("../.env")
# Check if all required environment variables are set
# This must happen before importing video which uses API keys without checking
#check_env_vars()


from video import make_meme

from time import sleep
import praw
import requests
import cv2
import numpy as np
import os
import pickle
import stdiomask

POST_SEARCH_AMOUNT = 50
UPLOAD_TO_YOUTUBE = False 
SLEEP_SEC_BETWEEN_UPLOADS = 60*60*32


# Create directory if it doesn't exist to save images
def create_folder(image_path):
    CHECK_FOLDER = os.path.isdir(image_path)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(image_path)

dir_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(dir_path, "reddit_scraper/images/")
ignore_path = os.path.join(dir_path, "reddit_scraper/ignore_images/")
create_folder(image_path)
def download_memes(reddit_client): 
    f_final = open("reddit_scraper/sub_list.csv", "r")
    #img_notfound = cv2.imread('./ignore_images/imageNF.png')
    for line in f_final:
        sub = line.strip()
        subreddit = reddit_client.subreddit(sub)

        print(f"Starting downloading from r/{sub}!")
        count = 0
        for submission in subreddit.new(limit=POST_SEARCH_AMOUNT):
            if "jpg" in submission.url.lower() or "png" in submission.url.lower():
                try:
                    resp = requests.get(submission.url.lower(), stream=True).raw
                    image = np.asarray(bytearray(resp.read()), dtype="uint8")
                    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                    # Could do transforms on images like resize!
                    compare_image = cv2.resize(image,(224,224))

                    # Get all images to ignore
                    for (dirpath, dirnames, filenames) in os.walk(ignore_path):
                        ignore_paths = [os.path.join(dirpath, file) for file in filenames]
                    ignore_flag = False

                    for ignore in ignore_paths:
                        ignore = cv2.imread(ignore)
                        difference = cv2.subtract(ignore, compare_image)
                        b, g, r = cv2.split(difference)
                        total_difference = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)
                        if total_difference == 0:
                            ignore_flag = True

                    if not ignore_flag:
                        cv2.imwrite(f"{image_path}{sub}-{submission.id}.png", image)
                        count += 1
                        print(f"Saved {count}")
                        
                except Exception as e:
                    print(f"Image failed. {submission.url.lower()}")
                    print(e)

print("If you can't login try deleting file 'token.pickle'")

def create_token():
    print("You need to enter your Reddit API crededentials.")
    creds = {}
    creds['client_id'] = input('client_id (needed): ')
    creds['client_secret'] = stdiomask.getpass(prompt="client_secret (needed): ")
    creds['user_agent'] = input('user_agent (can insert whatever): ')
    creds['username'] = input('username (can leave blank)')
    creds['password'] = stdiomask.getpass(prompt="password (can leave blank): ")
    return creds


# Get token file to log into reddit.
# You must enter your....
# client_id - client secret - user_agent - username password
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
else:
    creds = create_token()
    pickle_out = open("token.pickle","wb")
    pickle.dump(creds, pickle_out)


reddit = praw.Reddit(client_id=creds['client_id'],
                    client_secret=creds['client_secret'],
                    user_agent=creds['user_agent'],
                    username=creds['username'],
                    password=creds['password'])



print("Started")
memes_path= "reddit_scraper/images/"
output_path = "../meme.mp4"

directory_path = 'reddit_scraper/meme_bg'


# Choose the appropriate category ID for your videos
video_category_id = "24"  # Entertainment
privacyStatus = "public"  # "public", "private", "unlisted"
keywords = ["meme","humor","trend","viral","funny"]
yt_title = "#shorts #foryou #foryoupage #viral #xyzbca"
yt_desc = ""
video_metadata = {
    'video_path': os.path.abspath(output_path),
    'title': yt_title,
    'description': yt_desc,
    'category': video_category_id,
    'keywords': ",".join(keywords),
    'privacyStatus': privacyStatus,
}

while True:
    # List all files in the directory
    bgs = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    # Pick a random file
    random_bg = f"{directory_path}/{random.choice(bgs)}"

    memes = [f for f in os.listdir(memes_path) if os.path.isfile(os.path.join(memes_path, f))]

    if len(memes) == 0:
        print("Out of memes... downloading")
        download_memes(reddit)
        memes = [f for f in os.listdir(memes_path) if os.path.isfile(os.path.join(memes_path, f))]


    random_meme = f"{memes_path}{random.choice(memes)}"

    make_meme(random_bg,random_meme,output_path,0.6)
    os.remove(random_meme)

    if UPLOAD_TO_YOUTUBE:
        print("Uploading to youtube...")
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
    
    print(f"Sleeping for {SLEEP_SEC_BETWEEN_UPLOADS}s...")
    sleep(SLEEP_SEC_BETWEEN_UPLOADS)