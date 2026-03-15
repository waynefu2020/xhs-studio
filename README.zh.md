# xhs-studio

**中文 | [English](README.md)**

适用于 Claude Code 的小红书运营 Skill，覆盖从**搜索热点选题**到**一键发布图文**的完整工作流。

## 功能

- 🔍 **搜索热点** — 按关键词搜索小红书热门笔记，用于选题参考
- 📝 **发布图文** — 支持标题、正文、多图、话题标签、可见范围设置
- 📅 **定时发布** — 支持提前 1 小时至 14 天的定时发布
- 🔐 **扫码登录** — 二维码扫码登录，session 自动保存，支持随时切换账号

## 依赖

- Python 3.8+
- [`xiaohongshu-mcp`](https://github.com/jobsimi/xiaohongshu-mcp) 二进制文件

## 安装配置

### 1. 下载 xiaohongshu-mcp

前往 [xiaohongshu-mcp releases](https://github.com/jobsimi/xiaohongshu-mcp/releases) 下载对应平台的二进制文件，放到本地路径。

### 2. 配置 EXTEND.md

在项目目录创建 `.baoyu-skills/xhs-studio/EXTEND.md`，或全局配置 `~/.baoyu-skills/xhs-studio/EXTEND.md`：

```yaml
mcp_bin: /path/to/xiaohongshu-mcp-darwin-arm64
mcp_port: 18060
```

### 3. 登录账号

```bash
python3 scripts/login.py
```

用小红书 App 扫描弹出的二维码，登录成功后 session 自动保存，后续无需重复登录。

## 使用方法

### 搜索热点选题

```bash
python3 scripts/search.py "Claude Code"
python3 scripts/search.py "AI工具" --limit 20
```

输出热门笔记标题、作者、点赞数，用于内容选题参考。

### 发布图文笔记

```bash
python3 scripts/publish.py \
  --title "非技术人用AI Skill，我测了5个场景" \
  --content "正文内容..." \
  --images /path/to/cover.png \
  --tags "AI工具" "效率神器" "职场效率" \
  --visibility "公开可见"
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--title` | ✅ | 标题，最多 20 个中文字 |
| `--content` | ✅ | 正文内容，支持换行 |
| `--images` | ✅ | 图片路径（本地绝对路径 或 https:// 链接，最多 18 张） |
| `--tags` | 可选 | 话题标签，空格分隔多个 |
| `--visibility` | 可选 | `公开可见`（默认）/ `仅自己可见` / `仅互关好友可见` |
| `--schedule` | 可选 | 定时发布，ISO8601 格式，如 `2026-03-16T20:00:00+08:00` |

### 定时发布示例

```bash
python3 scripts/publish.py \
  --title "标题" \
  --content "正文" \
  --images cover.png \
  --schedule "2026-03-16T20:00:00+08:00"
```

### 切换账号

```bash
python3 scripts/login.py
```

已登录状态下运行会询问是否切换账号，确认后清除旧 session 并弹出新二维码。

## 在 Claude Code 中使用

安装此 Skill 后，直接用自然语言指令即可触发：

- `帮我搜索小红书热点`
- `帮我发小红书`
- `发布到小红书，仅自己可见`
- `定时发布这篇笔记到小红书`

## 注意事项

- MCP 服务未启动时会自动拉起，无需手动管理进程
- 系统代理环境下会自动设置 `NO_PROXY=localhost`，无需额外配置
- 标题限制：20 个中文字符
- 图片限制：单篇最多 18 张
- 定时发布范围：1 小时 ～ 14 天后

## 鸣谢

- [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) — 本 Skill 底层依赖的小红书 MCP 服务，由 [@xpzouying](https://github.com/xpzouying) 开发。
- [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) — 本 Skill 遵循的 Claude Code Skill 规范与框架，由 [@JimLiu](https://github.com/JimLiu) 开发。
