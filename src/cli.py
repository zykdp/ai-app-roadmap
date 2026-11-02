from __future__ import annotations

import argparse

from .cards import add_card, list_cards, search_cards


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cards", description="本地知识卡片")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="新增一张卡片")
    p_add.add_argument("title", help="标题")
    p_add.add_argument("content", help="内容")
    p_add.add_argument("--tag", action="append", default=[], help="标签，可重复")

    sub.add_parser("list", help="按时间倒序列出卡片")

    p_search = sub.add_parser("search", help="按关键词搜索")
    p_search.add_argument("keyword", help="关键词")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "add":
        card = add_card(args.title, args.content, tags=args.tag)
        print(f"[OK] 已添加：{card['title']} ({card['id'][:8]})")

    elif args.command == "list":
        cards = list_cards()
        if not cards:
            print("还没有卡片，先 add 一张。")
            return 0
        for index, card in enumerate(cards, 1):
            tags = " ".join(f"#{tag}" for tag in card.get("tags", []))
            print(f"{index}. {card['title']} {tags}".rstrip())
            print(f"   {card.get('content', '')[:80]}")

    else:
        cards = search_cards(args.keyword)
        print(f"找到 {len(cards)} 张卡片")
        for card in cards:
            print(f"- {card['title']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())