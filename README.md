# Anki Card Generator

Desktop app that auto-generates Anki flashcards from question screenshots — built for med students using UWorld and similar question banks.

## How it works

1. Get a question wrong on UWorld
2. Press `⌘ Shift G`
3. AI extracts the question, answer, and explanation from the screen
4. Card is automatically created and pushed to Anki

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
\`\`\`bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your OpenRouter API key to .env
uvicorn main:app --reload --port 8001
\`\`\`

### Frontend
\`\`\`bash
cd frontend
npm install
npm start
\`\`\`

## Status
MVP working — generates and pushes cards end-to-end. Built in one night.
