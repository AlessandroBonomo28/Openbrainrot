# Openbrainrot 😂
<img src="https://github.com/user-attachments/assets/e011f1e1-4e35-4826-b151-25e8578ea520" width="200" />

Automate the creation of brainrot clips, simply by providing a video topic to talk about.

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
