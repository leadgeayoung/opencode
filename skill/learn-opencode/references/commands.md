# 快捷命令

自定义斜杠命令，位于 `.opencode/command/<name>.md` 或 `opencode.json` 的 `command` 字段。

## 模板语法

| 占位符 | 说明 |
|--------|------|
| `$ARGUMENTS` | 全部参数 |
| `$1`, `$2`, ... | 位置参数 |
| `` !`command` `` | Shell 命令输出 |
| `@file` | 文件引用 |

## 示例

`.opencode/command/review.md`

```markdown
---
description: "审查指定文件的代码质量"
agent: plan
---
@$1
请审查这个文件的代码质量，重点关注：
1. 代码规范和命名
2. 潜在 Bug
3. 性能问题
4. 可维护性
```

使用：`/review src/main.ts`

`.opencode/command/find-logs.md`

```markdown
---
description: "搜索错误日志"
---
!grep -n "error" !`$1`
总结这些错误的关键模式和可能原因。
```
