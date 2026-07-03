---
name: learn-opencode
description: "OpenCode TUI AI coding assistant — install, model connect, agent/skill systems, daily workflow."
metadata:
  homepage: "https://learn-opencode.org"
---

# Learn OpenCode

## Workflow

1. **安装连接** — `curl -fsSL https://opencode.ai/install | bash` / `scoop install opencode` → 代理 → `opencode auth login` → 验证 `opencode --version`
2. **核心三件套** — `@` 引用文件/Agent · `!` 执行命令 · `/` 斜杠命令（`/help`、`/new`、`/models`、`/init`、`/compact`、`/theme`）
3. **选模式** — `Tab` 切换：**Build**（读写全部，写代码/改文件）vs **Plan**（只读，分析/规划/审查）。不确定用 Plan，确定了用 Build
4. **会话管理** — `Ctrl+X N` 新建 · `Ctrl+X L` 列表 · `Escape` 中断（×2 强制） · `/compact` / `Ctrl+X C` 压缩 · `Ctrl+T` 切换思考深度
5. **进阶配置** — 配置 `opencode.json` · Agent `.opencode/agent/<name>.md` · Skill `.opencode/skill/<name>/SKILL.md` · 规则 `AGENTS.md` · 命令 `.opencode/command/<name>.md` · MCP `mcpServers`

## Safety Rules

- 专用工具优先于 bash（有权限检查 + LSP 诊断）
- `rm/cp/mv` 自动检查路径是否在项目内
- 外部目录需配 `external_directory`
- 配置优先级：项目 > `$OPENCODE_CONFIG` > `~/.config/opencode/opencode.json` > 远程
- 凭证存 `auth.json`（XDG 规范），不硬编码 API Key

## References

`references/` — install, basics, config, agents, skills, workflow, commands, rules, mcp, advanced.
