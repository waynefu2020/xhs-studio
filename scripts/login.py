#!/usr/bin/env python3
"""
Login to Xiaohongshu via QR code.

Usage:
  python3 login.py
"""

import base64
import json
import os
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(__file__))
from _mcp import load_config, ensure_mcp_running, get_session, mcp_call


def login():
    config = load_config()
    url = ensure_mcp_running(config)
    sid = get_session(url)

    # Check current login status
    resp, _ = mcp_call(url, "tools/call", {"name": "check_login_status", "arguments": {}}, session_id=sid)
    status_text = resp.get("result", {}).get("content", [{}])[0].get("text", "")
    if "已登录" in status_text:
        print(status_text)
        ans = input("\nAlready logged in. Re-login with a different account? [y/N] ").strip().lower()
        if ans != "y":
            print("Login cancelled.")
            return

        # Delete cookies first
        mcp_call(url, "tools/call", {"name": "delete_cookies", "arguments": {}}, session_id=sid)
        print("✅ Previous session cleared.\n")

    # Get QR code
    resp2, _ = mcp_call(url, "tools/call", {"name": "get_login_qrcode", "arguments": {}}, session_id=sid)
    contents = resp2.get("result", {}).get("content", [])

    qr_saved = False
    for c in contents:
        if c.get("type") == "image":
            img_data = base64.b64decode(c["data"])
            qr_path = os.path.join(tempfile.gettempdir(), "xhs-qrcode.png")
            with open(qr_path, "wb") as f:
                f.write(img_data)
            # Open with system viewer
            subprocess.Popen(["open", qr_path])
            print(f"📱 QR code opened. Scan with Xiaohongshu app.")
            qr_saved = True
        elif c.get("type") == "text":
            print(c.get("text", ""))

    if not qr_saved:
        print("Failed to get QR code.")
        sys.exit(1)

    # Wait for login
    print("\nWaiting for scan", end="", flush=True)
    for _ in range(60):
        time.sleep(2)
        print(".", end="", flush=True)
        try:
            resp3, _ = mcp_call(url, "tools/call", {"name": "check_login_status", "arguments": {}}, session_id=sid)
            text = resp3.get("result", {}).get("content", [{}])[0].get("text", "")
            if "已登录" in text:
                print(f"\n\n✅ {text}")
                return
        except Exception:
            pass

    print("\n❌ Login timed out. Please try again.")
    sys.exit(1)


if __name__ == "__main__":
    login()
