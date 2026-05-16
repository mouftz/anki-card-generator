from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.vision import generate_anki_card
from services.anki import add_card, create_deck
import traceback

router = APIRouter()

class ScreenshotRequest(BaseModel):
    image_base64: str
    deck_name: str = "Wrong Answers"
    reason: str = "Knowledge gap"

@router.post("/generate-card")
async def generate_card(req: ScreenshotRequest):
    try:
        card = generate_anki_card(req.image_base64)
        
        if not card.get("is_question", False):
            return {
                "is_question": False,
                "reason": card.get("reason", "Not a medical question")
            }
        
        create_deck(req.deck_name)
        tags = [req.reason.lower().replace(" ", "_")]
        
        note_id = add_card(
            deck_name=req.deck_name,
            front=card["anki_front"],
            back=card["anki_back"],
            tags=tags
        )
        
        return {
            "is_question": True,
            "card": card,
            "anki_note_id": note_id,
            "deck": req.deck_name
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))