from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_cards(monkeypatch):
    monkeypatch.setattr(
        "src.api.list_cards",
        lambda: [
            {
                "id": "1",
                "title": "测试",
                "content": "内容",
                "tags": [],
                "created_at": "2026-01-01T00:00:00+00:00",
            }
        ],
    )

    response = client.get("/cards")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "测试"


def test_search_cards(monkeypatch):
    monkeypatch.setattr("src.api.search_cards", lambda q: [])

    response = client.get("/cards/search?q=rag")
    assert response.status_code == 200
    assert response.json() == []


def test_create_card(monkeypatch):
    def fake_add(title, content, tags):
        return {
            "id": "test-id",
            "title": title,
            "content": content,
            "tags": tags,
            "created_at": "2026-01-01T00:00:00+00:00",
        }

    monkeypatch.setattr("src.api.add_card", fake_add)

    response = client.post(
        "/cards",
        json={"title": "新卡片", "content": "内容", "tags": ["AI"]},
    )
    assert response.status_code == 201
    assert response.json()["id"] == "test-id"
    assert response.json()["tags"] == ["AI"]


def test_create_card_rejects_blank(monkeypatch):
    def fake_add(title, content, tags):
        raise ValueError("标题不能为空")

    monkeypatch.setattr("src.api.add_card", fake_add)

    response = client.post("/cards", json={"title": " ", "content": "内容"})
    assert response.status_code == 400
    assert response.json()["detail"] == "标题不能为空"


def test_create_card_validation_error():
    response = client.post("/cards", json={"title": "x", "content": ""})
    assert response.status_code == 422