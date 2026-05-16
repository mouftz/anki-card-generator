# MedDeck

Desktop app that auto-generates Anki flashcards from question screenshots — built for med students using UWorld and similar question banks.

## How it works

1. Get a question wrong on UWorld
2. Press `⌘ Shift G`
3. AI extracts the question, answer, and explanation from the screen
4. Card is automatically created and pushed to Anki
## Screenshots

**1. Question on screen — press the hotkey**

<img src="https://github.com/user-attachments/assets/96a4130a-9eab-4da0-8744-1f926883490d" width="700" />

**2. Review the AI-generated card**

<img src="https://github.com/user-attachments/assets/d59165e9-29e2-4bc1-a661-7941a15c1563" width="400" />

**3. Card lands in Anki automatically**

<img src="https://github.com/user-attachments/assets/599077e9-9682-4302-9432-9fd4323b9df7" width="600" />

## Stack

- Electron + React (desktop frontend)
- FastAPI (Python backend)
- OpenRouter API (Gemma 4 vision model for screenshot OCR)
- AnkiConnect (pushes cards directly to Anki)

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- [Anki](https://apps.ankiweb.net/) installed with [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on
- An [OpenRouter](https://openrouter.ai) API key (free tier works)

### Backend
~~~bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your OpenRouter API key to .env
uvicorn main:app --reload --port 8001
~~~

### Frontend
~~~bash
cd frontend
npm install
npm start
~~~