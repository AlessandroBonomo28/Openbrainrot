# Openbrainrot 😂
Automate the creation of brainrot clips, simply by providing a video topic to talk about.

<img src="https://github.com/user-attachments/assets/5d430ec4-aab4-4587-9479-d12000468794" width="350"  />

> **🎥** Watch the video on my [YouTube channel](https://www.youtube.com/@coding.emojii).

Check out the **instructions for running locally** [here](Local.md).

## FAQ 🤔

### How do I replace the default background clips?

Go to `Backend/backgrounds` folder and replace the `.mp4` files.
⚠️ Files should be **at least 1 minute long** ⚠️ otherwise the 
voice over will not fit. The background will be automatically clipped
so you can even upload 2 minutes long background clips and play with 
the **paragraph number** parameter.

### How do I get the TikTok session ID?

You can obtain your TikTok session ID by logging into TikTok in your browser and copying the value of the `sessionid` cookie.

### My ImageMagick binary is not being detected

Make sure you set your path to the ImageMagick binary correctly in the `.env` file, it should look something like this:

```env
IMAGEMAGICK_BINARY="C:\\Program Files\\ImageMagick-7.1.0-Q16\\magick.exe"
```

Don't forget to use double backslashes (`\\`) in the path, instead of one.

### I can't install `playsound`: Wheel failed to build

If you're having trouble installing `playsound`, you can try installing it using the following command:

```bash
pip install -U wheel
pip install -U playsound
```

If you were not able to find your solution, please ask in the discord or create a new issue, so that the community can help you.

## Donate 🎁

If you like and enjoy `Openbrainrot😂`, and would like to donate to help grow the yt channel you can [buy me a coffee](https://buymeacoffee.com/servizibon0) ☕

## Contributing 🤝

Do whatever you want 😂

## License and credits 📝

See [`LICENSE`](LICENSE) file for more information.

`Openbrainrot😂` is a fork of [MoneyPrinter](https://github.com/FujiwaraChoki/MoneyPrinter) originally made by [FujiwaraChoki](https://github.com/FujiwaraChoki)


## Extra instructions for help 👍
### linux install magick
```
wget https://download.imagemagick.org/ImageMagick/download/ImageMagick.tar.gz
tar -xvzf ImageMagick.tar.gz
cd ImageMagick-7.0.11-14/
./configure
sudo make
sudo make install
```
#### now add magick path to .env
```
IMAGEMAGICK_BINARY="/usr/local/bin/magick"
```
## Automatic YouTube Uploading 🎥

Openbrainrot now includes functionality to automatically upload generated videos to YouTube.

To use this feature, you need to:

1. Create a project inside your Google Cloud Platform -> [GCP](https://console.cloud.google.com/).
2. Obtain `client_secret.json` from the project and add it to the Backend/ directory.
3. Enable the YouTube v3 API in your project -> [GCP-API-Library](https://console.cloud.google.com/apis/library/youtube.googleapis.com)
4. Create an `OAuth consent screen` and add yourself (the account of your YouTube channel) to the testers.
5. Enable the following scopes in the `OAuth consent screen` for your project:

```
'https://www.googleapis.com/auth/youtube'
'https://www.googleapis.com/auth/youtube.upload'
'https://www.googleapis.com/auth/youtubepartner'
```

6. Add to authorized urls in **Youtube data API V3**

```
http://localhost:8080/
http://localhost:8080/oauth2callback
```

After this, you can generate the videos and you will be prompted to authenticate yourself.

The authentication process creates and stores a `main.py-oauth2.json` file inside the Backend/ directory. Keep this file to maintain authentication, or delete it to re-authenticate (for example, with a different account).

Videos are uploaded as private by default. For a completely automated workflow, change the privacyStatus in main.py to your desired setting ("public", "private", or "unlisted").

For videos that have been locked as private due to upload via an unverified API service, you will not be able to appeal. You’ll need to re-upload the video via a verified API service or via the YouTube app/site. The unverified API service can also apply for an API audit. So make sure to verify your API, see [OAuth App Verification Help Center](https://support.google.com/cloud/answer/13463073) for more information.

