# xhs-studio

A Claude Code skill for publishing image-text notes to Xiaohongshu (小红书) and searching trending content.

## Features

- 📝 Publish image-text notes with title, body, tags, and images
- 🔍 Search trending notes by keyword
- 📅 Schedule posts (1 hour to 14 days ahead)
- 👁️ Visibility control (public / private / friends only)
- 🔐 QR code login with persistent session

## Requirements

- Python 3.8+
- [`xiaohongshu-mcp`](https://github.com/jobsimi/xiaohongshu-mcp) binary

## Setup

### 1. Download xiaohongshu-mcp

Download the binary for your platform from [xiaohongshu-mcp releases](https://github.com/jobsimi/xiaohongshu-mcp/releases) and place it somewhere accessible.

### 2. Configure EXTEND.md

Create `.baoyu-skills/xhs-studio/EXTEND.md` in your project (or `~/.baoyu-skills/xhs-studio/EXTEND.md` for global use):

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

### Publish a note

```bash
python3 scripts/publish.py \
  --title "非技术人用AI Skill，我测了5个场景" \
  --content "正文内容..." \
  --images /path/to/cover.png \
  --tags "AI工具" "效率神器" \
  --visibility "公开可见"
```

### Schedule a post

```bash
python3 scripts/publish.py \
  --title "标题" \
  --content "正文" \
  --images cover.png \
  --schedule "2026-03-16T20:00:00+08:00"
```

### Search trending content

```bash
python3 scripts/search.py "Claude Code"
python3 scripts/search.py "AI工具" --limit 20
```

## Using with Claude Code

Install this skill and Claude Code will automatically use it when you say:

- "帮我发小红书"
- "Post to XHS"
- "搜索小红书热点"
- "发布到小红书"

## Notes

- Title max: 20 Chinese characters
- Images max: 18 per post
- Proxy: `NO_PROXY=localhost` is set automatically to bypass system proxies
- The MCP server starts automatically if not running
