# Openbrainrot 😂 - Running locally

Automate the creation of brain rot clips locally, simply by providing a video topic to talk about.

> **🎥** Watch the video on my [YouTube channel](https://www.youtube.com/@coding.emojii).

## Installation 📥

`Openbrainrot` requires Python 3.11 to run effectively. If you don't have Python installed, you can download it from [here](https://www.python.org/downloads/).

After you finished installing Python, you can install `Openbrainrot😂` by following the steps below:

```bash
git clone https://github.com/AlessandroBonomo28/Openbrainrot.git
cd Openbrainrot

# Install requirements
pip install -r requirements.txt

# Copy .env.example and fill out values
cp .env.example .env

# Run the backend server
cd Backend
python brainrot.py

# Run the frontend server
cd ../Frontend
python -m http.server 3000
```

See [`.env.example`](.env.example) for the required environment variables.

If you need help, open [EnvironmentVariables.md](EnvironmentVariables.md) for more information.

## Usage 🛠️

1. Copy the `.env.example` file to `.env` and fill in the required values
1. Open `http://localhost:3000` in your browser
1. Enter a topic to talk about
1. Click on the "Generate" button
1. Wait for the video to be generated
1. The video's location is `Openbrainrot/output.mp4`

