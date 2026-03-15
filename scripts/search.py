#!/usr/bin/env python3
"""
Search trending notes on Xiaohongshu (小红书).

Usage:
  python3 search.py "AI工具"
  python3 search.py "Claude Code" --limit 20
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _mcp import load_config, ensure_mcp_running, get_session, mcp_call


def search(keyword, limit=10):
    config = load_config()
    url = ensure_mcp_running(config)
    sid = get_session(url)

    resp, _ = mcp_call(url, "tools/call", {
        "name": "search_feeds",
        "arguments": {"keyword": keyword}
    }, session_id=sid)

    text = resp.get("result", {}).get("content", [{}])[0].get("text", "")
    try:
        data = json.loads(text)
        feeds = data.get("feeds", [])[:limit]
    except Exception:
        print(text[:500])
        return

    print(f"\n🔍 Results for「{keyword}」({len(feeds)} notes)\n")
    for i, item in enumerate(feeds, 1):
        card = item.get("noteCard", {})
        user = card.get("user", {})
        interact = card.get("interactInfo", {})
        note_type = "📹" if card.get("type") == "video" else "📝"
        print(f"{i}. {note_type} {card.get('displayTitle', '(no title)')}")
        print(f"   👤 {user.get('nickname', '-')}   ❤️  {interact.get('likedCount', '-')}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Xiaohongshu trending content")
    parser.add_argument("keyword", help="Search keyword")
    parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    args = parser.parse_args()
    search(args.keyword, args.limit)
