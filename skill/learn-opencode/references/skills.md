# Skill 系统

Skill 是触发器驱动的专业知识包，采用渐进式披露（Progressive Disclosure）设计。

## 目录结构

```
.opencode/skill/<name>/
  SKILL.md              # 主文件（name + description 必填）
  references/           # 详细文档（按需加载）
  scripts/              # 辅助脚本（按需运行）
  assets/               # 模板/资源文件
  agents/               # UI 元数据
```

## 搜索位置（依次）

1. `.opencode/skill/`（项目级）
2. `~/.config/opencode/skill/`（全局）
3. `.claude/skills/`（Claude Code 兼容）
4. `~/.claude/skills/`

## 三层加载机制

1. **Frontmatter**（name + description，~100 词）— 始终可见，决定是否触发
2. **SKILL.md 正文** — 任务匹配时加载
3. **references/ 目录** — 需要具体细节时按需加载

## SKILL.md 模板

```markdown
---
name: skill-name
description: "一句话核心能力。适用：X、Y。不适用：Z。"
---

用 1-2 行说明本 Skill 用途。

## Workflow

1. 步骤一
2. 步骤二
3. 步骤三
```

## Skill 权限管控

```json
{
  "permission": {
    "skill": {
      "pr-review": "allow",
      "internal-*": "deny"
    }
  }
}
```

Skill vs AGENTS.md：Skill 按需加载（节省上下文），AGENTS.md 始终加载（适合项目规范）。
