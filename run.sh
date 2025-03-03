#!/bin/bash

echo starting fake display for opening google-chrome auth screen
export DISPLAY=:1
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
Xvfb :1 -screen 0 1024x768x16 &

# BRAINROT UPLOADER 
#sleep 1
#echo launching 2 backends and brainrot backend invoker - brainrot uploader
cd /home/username/Openbrainrot/Backend
source /home/username/Openbrainrot/env/bin/activate

# BRAINROT UPLOADER 
#python /home/username/openbrainrot/Backend/brainrot.py & 
#python /home/username/openbrainrot/Backend/brainrot_uploader.py

# REDDIT MEME UPLOADER
python /home/username/Openbrainrot/Backend/reddit_meme_uploader.py
