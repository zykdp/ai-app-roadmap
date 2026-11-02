from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .cards import add_card, delete_card, get_card, list_cards, search_cards

app = FastAPI(title="AI 学习卡片 API", version="0.1.0")


class CardIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)


class CardOut(CardIn):
    id: str
    created_at: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/cards", response_model=list[CardOut])
def get_cards() -> list[dict]:
    return list_cards()


@app.get("/cards/search", response_model=list[CardOut])
def search(q: str) -> list[dict]:
    return search_cards(q)


@app.post("/cards", response_model=CardOut, status_code=201)
def create_card(payload: CardIn) -> dict:
    try:
        return add_card(payload.title, payload.content, payload.tags)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/cards/{card_id}", response_model=CardOut)
def read_card(card_id: str) -> dict:
    card = get_card(card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="卡片不存在")
    return card


@app.delete("/cards/{card_id}", status_code=204)
def remove_card(card_id: str) -> None:
    if not delete_card(card_id):
        raise HTTPException(status_code=404, detail="卡片不存在")