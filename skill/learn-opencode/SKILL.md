---
name: learn-opencode
description: "Complete OpenCode knowledge base: install, configure, daily use, scenarios, agents, skills, MCP, enterprise, and all advanced features."
---

# OpenCode 知识库

## 核心架构

| 组件 | 说明 |
|------|------|
| **Build** (Primary Agent) | 默认助手，读写模式，所有工具可用 |
| **Plan** (Primary Agent) | 只读模式，仅允许编辑 `.opencode/plans/*.md` |
| **Explore** (Subagent) | 代码探索，@explore 调用，深度: quick/medium/very thorough |
| **General** (Subagent) | 通用研究，@general 调用，多步任务 |
| 隐藏 Agent: title/summary/compaction | 自动运行，生成标题/摘要/压缩 |

## 三键操作

| 键 | 作用 | 示例 |
|----|------|------|
| `@` | 引用文件/Agent | `@src/main.ts` / `@explore` |
| `!` | 执行命令 | `!git status` |
| `/` | 斜杠命令 | `/new` `/help` `/models` |

## 6大核心工具

| 工具 | 功能 | 关键参数/限制 |
|------|------|--------------|
| **read** | 读取文件/目录 | `offset`(0-based), `limit`(默认2000行), 支持图片/PDF |
| **write** | 创建/覆写文件 | 必须先 read 后 write，自动 LSP 诊断 |
| **edit** | 精确字符串替换 | 9层智能匹配策略，`replaceAll` 批量替换 |
| **bash** | 执行命令 | `timeout` 默认 2min, `workdir`, 输出截断 50KB/2000行 |
| **grep** | 搜索文件内容 | 正则支持，上限 100 条 |
| **glob** | 搜索文件名 | glob 模式，上限 100 条 |

## 配置加载优先级 (低→高)

1. Remote `.well-known/opencode` → 2. `~/.config/opencode/opencode.json` → 3. `$OPENCODE_CONFIG` → 4. `./opencode.json` → 5. `./.opencode/opencode.json` → 6. `$OPENCODE_CONFIG_CONTENT` → 7. Managed config

## 内网部署环境变量

| 变量 | 作用 |
|------|------|
| `OPENCODE_DISABLE_MODELS_FETCH=true` | 禁用模型列表拉取 |
| `OPENCODE_MODELS_PATH=~/.cache/opencode/models.json` | 本地模型列表路径 |
| `OPENCODE_MODELS_URL=https://internal-mirror` | 内部 models.dev 镜像 |
| `OPENCODE_DISABLE_DEFAULT_PLUGINS=true` | 禁用内置插件安装 |
| `OPENCODE_DISABLE_AUTOUPDATE=true` | 禁用自动更新 |
| `OPENCODE_DISABLE_LSP_DOWNLOAD=true` | 禁用 LSP 下载 |
| `OPENCODE_DISABLE_PROJECT_CONFIG=true` | 禁用项目级配置扫描 |

## 完整参考

详见 `references/` 目录下各文件：

| 文件 | 内容 |
|------|------|
| 01-getting-started | 安装/网络/11种模型连接 |
| 02-daily-usage | TUI/工具/会话/快捷键/全局规则 |
| 03-workflow | Plan/Build/Agent/init |
| 04-coder-scenarios | 开发者场景全集 |
| 05-writer-scenarios | 写作者场景全集 |
| 06-office-scenarios | 办公场景全集 |
| 07-configuration | 配置系统完整参考 |
| 08-agents | Agent 创建/设计模式/权限 |
| 09-skills | Skills 系统/5种设计模式/分发 |
| 10-commands | 自定义命令 |
| 11-permissions | 权限控制 |
| 12-themes-keybinds | 主题与快捷键 |
| 13-mcp | MCP 基础/高级/Chrome |
| 14-ide-integration | IDE 集成全集 |
| 15-remote-mode | 远程模式 |
| 16-sdk | SDK 开发 |
| 17-enterprise-offline | 企业/内网部署 |
| 18-plugins-hooks | 插件与 Hooks |
| 19-custom-tools-formatters | 自定义工具/LSP/格式化 |
| 20-github-gitlab-share | GitHub/GitLab/Share |
| 21-compaction-thinking | 压缩/思维深度/调试等 |
| 22-appendix-complete | 附录全集 |
