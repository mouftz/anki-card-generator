from fastapi import FastAPI
from routes.card import router as card_router

app = FastAPI()
app.include_router(card_router)

@app.get("/")
def root():
    return {"status": "ok"}