# Lyrics Retrieval API 🎵

A robust API service that retrieves song lyrics by artist and title. Built with FastAPI, this service scrapes and processes lyrics from Genius.com, providing clean, formatted text output.

## Features ✨

- 🔍 Fetch lyrics by artist and song title
- 🧹 Advanced text processing and cleaning
- 🌐 Genius.com integration
- ⚡ FastAPI performance
- 🛡️ Error handling for missing lyrics

## Future Game Integration 🎮
*Planned features for the interactive lyrics game:*
- 🎵 Guess-the-missing-word gameplay
- ⏱️ Timed challenges
- 📊 Score tracking
- 🏆 Leaderboards

## Tech Stack 🛠️

**Backend:**
- Python 3.8+
- FastAPI (Web framework)
- BeautifulSoup4 (Web scraping)
- Requests (HTTP client)

**Text Processing:**
- Regular expressions
- Advanced string manipulation
- Multi-line text normalization

## Installation 💻

### Prerequisites
- Python 3.8+
- Spotify Developer account
- Ngrok account (auth token in .env)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ranuncolo95/song_quiz.git
   cd song_quiz

2. Install dependencies:

   ```bash
    pip install -r requirements.txt

3. Setup the evironment variables.

   ```bash

      #.env file in data/utils/.env

      SPOTIFY_CLIENT_ID='your_spotify_client_id'
      SPOTIFY_CLIENT_SECRET='your_spotify_client_secret'
      #this will be modified in automatic
      SPOTIFY_REDIRECT_URI=""
      NGROK_AUTHTOKEN='ngrok_auth_token'
  
4. Run the ngrok script:

   ```bash
    py ngrok_start.py

5. Get the link in Spotify Dashboard

Copy the Active Public URL given by the script in the Spotify Dev Dashboard in the Redirect URI, with /callback at the end.

6. Run the main script

   ```bash
      py main.py

6. Visit the local url given by FastAPI and enjoy the lyrics!
