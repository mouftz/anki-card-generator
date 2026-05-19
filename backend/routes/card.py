from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.vision import generate_anki_card
from services.anki import add_card, create_deck
import traceback

router = APIRouter()

class ScreenshotRequest(BaseModel):
    image_base64: str

class SaveCardRequest(BaseModel):
    anki_front: str
    anki_back: str
    deck_name: str = "Wrong Answers"
    reason: str = "Knowledge gap"

@router.post("/generate-card")
async def generate_card(req: ScreenshotRequest):
    """Just generates the card, doesn't push to Anki."""
    try:
        card = generate_anki_card(req.image_base64)
        return card
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save-card")
async def save_card(req: SaveCardRequest):
    """Pushes a (possibly edited) card to Anki."""
    try:
        create_deck(req.deck_name)
        tags = [req.reason.lower().replace(" ", "_")]
        
        note_id = add_card(
            deck_name=req.deck_name,
            front=req.anki_front,
            back=req.anki_back,
            tags=tags
        )
        
        return {
            "anki_note_id": note_id,
            "deck": req.deck_name
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))