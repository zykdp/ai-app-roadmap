import uuid
from datetime import datetime, timezone
"""知识卡片的 JSON 存取。"""

import json
from pathlib import Path

# cards.py 在 src/ 下，往上两级才是项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "cards.json"


def load_cards(path: Path = DATA_FILE) -> list[dict]:
    """读取卡片；文件不存在返回空列表。"""
    if not path.exists():
        return []

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"卡片文件不是合法 JSON: {path}") from exc

    if not isinstance(data, list):
        raise ValueError("卡片文件顶层必须是列表")

    return data


def save_cards(cards: list[dict], path: Path = DATA_FILE) -> None:
    """保存卡片；自动创建 data 目录。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(cards, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")
def add_card(
    title: str,
    content: str,
    tags: list[str] | None = None,
    path: Path = DATA_FILE,
) -> dict:
    """新增一张卡片并保存，返回新卡片。"""
    title = title.strip()
    content = content.strip()
    if not title:
        raise ValueError("标题不能为空")
    if not content:
        raise ValueError("内容不能为空")
    if tags is None:
        tags = []
    if not isinstance(tags, list):
        raise ValueError("tags 必须是列表")

    card = {
        "id": uuid.uuid4().hex,
        "title": title,
        "content": content,
        "tags": [str(tag).strip() for tag in tags if str(tag).strip()],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    cards = load_cards(path)
    cards.append(card)
    save_cards(cards, path)
    return card


def list_cards(path: Path = DATA_FILE) -> list[dict]:
    """按创建时间倒序返回全部卡片。"""
    cards = load_cards(path)
    return sorted(cards, key=lambda c: c.get("created_at", ""), reverse=True)


def search_cards(keyword: str, path: Path = DATA_FILE) -> list[dict]:
    """在标题和内容中搜索，忽略大小写。"""
    keyword = keyword.strip().lower()
    if not keyword:
        return []

    result = []
    for card in load_cards(path):
        title = str(card.get("title", "")).lower()
        content = str(card.get("content", "")).lower()
        if keyword in title or keyword in content:
            result.append(card)
    return result