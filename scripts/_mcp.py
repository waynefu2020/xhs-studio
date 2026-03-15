"""
Shared MCP client utilities for xhs-studio skill.
"""

import json
import os
import subprocess
import time
import urllib.request

os.environ["NO_PROXY"] = "localhost"
os.environ["no_proxy"] = "localhost"


def load_config():
    """Load EXTEND.md config (project-level first, then user-level)."""
    paths = [
        os.path.join(os.getcwd(), ".baoyu-skills/xhs-studio/EXTEND.md"),
        os.path.expanduser("~/.baoyu-skills/xhs-studio/EXTEND.md"),
    ]
    for path in paths:
        if os.path.exists(path):
            config = {}
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if ":" in line and not line.startswith("#"):
                        k, _, v = line.partition(":")
                        config[k.strip()] = v.strip()
            return config
    return {}


def get_mcp_url(config):
    port = config.get("mcp_port", "18060")
    return f"http://localhost:{port}/mcp"


def ensure_mcp_running(config):
    """Start MCP server if not already running."""
    url = get_mcp_url(config)
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps({"jsonrpc": "2.0", "id": 0, "method": "ping", "params": {}}).encode(),
            headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=2)
        return url
    except Exception:
        pass

    mcp_bin = config.get("mcp_bin", "")
    if not mcp_bin or not os.path.exists(mcp_bin):
        raise RuntimeError(
            f"MCP binary not found: '{mcp_bin}'\n"
            "Please set 'mcp_bin' in .baoyu-skills/xhs-studio/EXTEND.md"
        )

    port = config.get("mcp_port", "18060")
    print(f"⏳ Starting xiaohongshu-mcp on port {port}...")
    subprocess.Popen(
        [mcp_bin, "-port", f":{port}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=os.path.dirname(mcp_bin),
    )
    time.sleep(3)
    return url


def mcp_call(url, method, params=None, session_id=None):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(
        url,
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read()), r.headers.get("Mcp-Session-Id")


def get_session(url):
    _, sid = mcp_call(url, "initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "xhs-studio", "version": "1.0"},
    })
    return sid
