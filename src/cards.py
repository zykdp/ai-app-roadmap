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