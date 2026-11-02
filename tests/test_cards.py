import json

import pytest

from src.cards import load_cards, save_cards


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