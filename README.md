# Lyrics Retrieval API 🎵

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)](https://fastapi.tiangolo.com/)

A robust API service that retrieves song lyrics by artist and title. Built with FastAPI, this service scrapes and processes lyrics from Genius.com, providing clean, formatted text output.

## Features ✨

- 🔍 Fetch lyrics by artist and song title
- 🧹 Advanced text processing and cleaning
- 🌐 Genius.com integration
- ⚡ FastAPI performance
- 🛡️ Error handling for missing lyrics
- 📦 Ready for deployment

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
- Poetry (recommended) or pip

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ranuncolo95/lyrics_api.git
   cd lyrics_api

2. Install dependencies:

   ```bash
    pip install -r requirements.txt
  
3. Run the development server:

   ```bash
    poetry run uvicorn main:app --reload





