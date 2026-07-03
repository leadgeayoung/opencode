# 规则文件 (AGENTS.md)

## 作用域

- `~/.config/opencode/AGENTS.md` — 全局（所有项目）
- 项目根目录 `AGENTS.md` — 项目级
- `opencode.json` 的 `instructions` 字段 — 引用多个文件

## 加载顺序（低→高）

全局 CLAUDE.md < 全局 AGENTS.md < 项目 AGENTS.md < instructions 文件

## instructions 字段

```json
{
  "instructions": [
    "AGENTS.md",
    ".opencode/rules/*.md",
    "https://example.com/team-rules.md",
    "/absolute/path/to/rules.md"
  ]
}
```

支持 glob 模式、URL、绝对路径。

## 细节

- **热加载**：规则文件修改后立即生效；`instructions` 路径列表需新会话
- **兼容文件名**：`AGENTS.md`（推荐）、`CLAUDE.md`（Claude Code 兼容）、`CONTEXT.md`（已废弃）
- **AI 风格规范**：规则文件可定义代码风格、架构约定、安全规范
