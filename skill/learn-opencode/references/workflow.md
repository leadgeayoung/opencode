# 工作流

## Plan vs Build

- **Plan** — 角色：架构师/审查者；权限：只读（仅编辑 `plans/*.md`）；场景：分析、规划、审查、探索；切换：Tab
- **Build** — 角色：实施者；权限：全部允许；场景：写代码、修 Bug、重构；切换：Tab

最佳实践：不确定用 Plan，确定了用 Build。

## /init 项目初始化

`/init` 命令让 AI 分析项目并生成 `.opencode/rules/` 下的配置文件。

## TODO 跟踪

告诉 AI "用 TODO 跟踪进度"，AI 自动创建任务清单管理复杂任务。

## 会话导航

- `/new` — 新会话
- 会话列表：`Ctrl+X L`
- 会话命名：自动生成标题，可手动修改

## 上下文压缩

- **Prune**：保留最近 40K tokens 工具输出，清除更早的
- **Summarize**：LLM 生成摘要替换历史消息
- 手动触发：`/compact` 或 `Ctrl+X C`
- 自动触发：接近上下文限制时自动

Context 百分比：(input + output + reasoning + cache.read + cache.write) / model.limit.context * 100
