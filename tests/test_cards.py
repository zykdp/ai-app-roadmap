import json

import pytest

from src.cards import (
    add_card,
    list_cards,
    load_cards,
    save_cards,
    search_cards,
)


def test_load_missing_file_returns_empty(tmp_path):
    assert load_cards(tmp_path / "cards.json") == []


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "nested" / "cards.json"
    cards = [{"id": "1", "title": "测试", "content": "内容"}]

    save_cards(cards, path)

    assert path.exists()
    assert load_cards(path) == cards


def test_load_invalid_json_raises(tmp_path):
    path = tmp_path / "cards.json"
    path.write_text("{not json", encoding="utf-8")

    with pytest.raises(ValueError):
        load_cards(path)


def test_load_non_list_raises(tmp_path):
    path = tmp_path / "cards.json"
    path.write_text(json.dumps({"a": 1}), encoding="utf-8")

    with pytest.raises(ValueError):
        load_cards(path)
def test_add_card_persists(tmp_path):
    path = tmp_path / "cards.json"

    card = add_card("RAG 是什么", "检索增强生成", ["AI"], path=path)

    assert card["id"]
    assert card["title"] == "RAG 是什么"
    assert load_cards(path)[0]["id"] == card["id"]


def test_add_card_rejects_empty(tmp_path):
    path = tmp_path / "cards.json"

    with pytest.raises(ValueError):
        add_card("  ", "内容", path=path)

    with pytest.raises(ValueError):
        add_card("标题", "  ", path=path)


def test_list_cards_newest_first(tmp_path):
    path = tmp_path / "cards.json"
    save_cards(
        [
            {"id": "old", "title": "旧", "content": "1", "created_at": "2026-01-01T00:00:00+00:00"},
            {"id": "new", "title": "新", "content": "2", "created_at": "2026-02-01T00:00:00+00:00"},
        ],
        path,
    )

    assert [card["id"] for card in list_cards(path)] == ["new", "old"]


def test_search_cards_ignores_case(tmp_path):
    path = tmp_path / "cards.json"
    add_card("FastAPI 入门", "学习 RAG 和 API", path=path)

    assert len(search_cards("rag", path)) == 1
    assert len(search_cards("fastapi", path)) == 1
    assert search_cards("", path) == []