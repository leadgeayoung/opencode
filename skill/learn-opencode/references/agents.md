# Agent 系统

## 内置 Agent

| Agent | 类型 | 权限 | 用途 |
|-------|------|------|------|
| **Build** | Primary | 全部允许 | 写代码、改文件（默认） |
| **Plan** | Primary | 只读（仅允许 `.opencode/plans/*.md`） | 分析、规划、审查 |
| **Explore** | Subagent | 只读（grep/glob/read） | 快速代码探索 |
| **General** | Subagent | 多任务 | 复杂研究、多步骤 |
| **compaction** | Internal | 自动 | 上下文压缩 |
| **title** | Internal | 自动 | 会话标题生成 |
| **summary** | Internal | 自动 | 会话摘要 |

## 自定义 Agent

**Markdown 方式**：`.opencode/agent/<name>.md`

```markdown
---
description: "审查 TypeScript 代码质量"
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.3
---

你是一个 TypeScript 代码审查专家。关注类型安全、错误处理和性能。
```

**JSON 方式**：`opencode.json` 的 `agent` 字段

文件名即 Agent 名称：`docs-writer.md` → Agent 名为 `docs-writer`。

## Frontmatter 字段

| 字段 | 说明 |
|------|------|
| `description` | 简短描述（影响自动选择） |
| `mode` | `subagent` / `primary` / `all` |
| `model` | `provider/model-id` |
| `temperature` | 0~1 |
| `steps` | 最大迭代步数 |
| `hidden` | `true/false` |
| `color` | 标签颜色 `"#RRGGBB"` |
| `permission.edit` | `deny` / `ask` / `allow` |

子代理 Session 隔离：子代理运行在独立 Session，看不到主 Agent 历史，调用时必须提供完整上下文。

调用方式：
- Primary Agent：`Tab` 键切换
- Subagent：`@agent名` 手动调用，或主 Agent 自动调用
- Agent 列表：`Ctrl+X A`
