#!/usr/bin/env python3
"""
Publish an image-text note to Xiaohongshu (小红书).

Usage:
  python3 publish.py --title "标题" --content "正文" --images img.png --tags "AI工具"
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _mcp import load_config, ensure_mcp_running, get_session, mcp_call


def publish(title, content, images, tags=None, visibility="公开可见", schedule_at=None):
    config = load_config()
    url = ensure_mcp_running(config)
    sid = get_session(url)

    args = {
        "title": title,
        "content": content,
        "images": images,
        "visibility": visibility,
    }
    if tags:
        args["tags"] = tags
    if schedule_at:
        args["schedule_at"] = schedule_at

    resp, _ = mcp_call(url, "tools/call", {"name": "publish_content", "arguments": args}, session_id=sid)
    result_text = resp.get("result", {}).get("content", [{}])[0].get("text", "")
    is_error = resp.get("result", {}).get("isError", False)

    if is_error or "失败" in result_text:
        print(f"❌ Publish failed: {result_text}")
        sys.exit(1)

    print(f"✅ Published successfully!")
    print(f"   Title      : {title}")
    print(f"   Images     : {len(images)}")
    print(f"   Tags       : {tags or []}")
    print(f"   Visibility : {visibility}")
    if schedule_at:
        print(f"   Scheduled  : {schedule_at}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish to Xiaohongshu")
    parser.add_argument("--title", required=True, help="Title (max 20 Chinese chars)")
    parser.add_argument("--content", required=True, help="Post body text")
    parser.add_argument("--images", required=True, nargs="+", help="Image paths or URLs")
    parser.add_argument("--tags", nargs="*", help="Topic tags")
    parser.add_argument("--visibility", default="公开可见",
                        choices=["公开可见", "仅自己可见", "仅互关好友可见"])
    parser.add_argument("--schedule", dest="schedule_at", help="Schedule time (ISO8601)")

    args = parser.parse_args()
    publish(args.title, args.content, args.images, args.tags, args.visibility, args.schedule_at)
