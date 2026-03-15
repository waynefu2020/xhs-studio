# xhs-studio

**[中文](README.zh.md) | English**

A Claude Code Skill for Xiaohongshu (小红书) — covering the full content workflow from trending topic discovery to one-click publishing.

## Features

- 🔍 **Trend Search** — Search trending notes by keyword for topic inspiration
- 📝 **Publish Notes** — Post image-text notes with title, body, images, tags, and visibility
- 📅 **Scheduled Posts** — Schedule publishing from 1 hour to 14 days ahead
- 🔐 **QR Code Login** — Scan to login, session auto-saved, easy account switching

## Requirements

- Python 3.8+
- [`xiaohongshu-mcp`](https://github.com/jobsimi/xiaohongshu-mcp) binary

## Setup

### 1. Download xiaohongshu-mcp

Download the binary for your platform from [xiaohongshu-mcp releases](https://github.com/jobsimi/xiaohongshu-mcp/releases).

### 2. Configure EXTEND.md

Create `.baoyu-skills/xhs-studio/EXTEND.md` in your project, or `~/.baoyu-skills/xhs-studio/EXTEND.md` for global use:

```yaml
mcp_bin: /path/to/xiaohongshu-mcp-darwin-arm64
mcp_port: 18060
```

### 3. Login

```bash
python3 scripts/login.py
```

Scan the QR code with your Xiaohongshu app. Session is saved automatically.

## Usage

### Search trending topics

```bash
python3 scripts/search.py "Claude Code"
python3 scripts/search.py "AI工具" --limit 20
```

### Publish a note

```bash
python3 scripts/publish.py \
  --title "标题（max 20 Chinese chars）" \
  --content "Post body..." \
  --images /path/to/cover.png \
  --tags "AI工具" "效率神器" \
  --visibility "公开可见"
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--title` | ✅ | Title, max 20 Chinese characters |
| `--content` | ✅ | Body text, supports line breaks |
| `--images` | ✅ | Image paths or https:// URLs (max 18) |
| `--tags` | optional | Topic tags, space-separated |
| `--visibility` | optional | `公开可见` (default) / `仅自己可见` / `仅互关好友可见` |
| `--schedule` | optional | Schedule time in ISO8601: `2026-03-16T20:00:00+08:00` |

### Switch accounts

```bash
python3 scripts/login.py
```

### Use with Claude Code

After installing this skill, trigger it with natural language:

- `帮我搜索小红书热点`
- `帮我发小红书`
- `Post to Xiaohongshu`
- `Search trending XHS content`

## Notes

- MCP server starts automatically if not running
- `NO_PROXY=localhost` is set automatically to bypass system proxies
- Title limit: 20 Chinese characters
- Image limit: 18 per post
- Schedule range: 1 hour – 14 days from now

## Acknowledgements

- [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) — The MCP server that powers Xiaohongshu automation in this skill. Built by [@xpzouying](https://github.com/xpzouying).
- [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) — The Claude Code Skill framework and conventions that this skill follows. Built by [@JimLiu](https://github.com/JimLiu).
