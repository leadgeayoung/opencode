# 配置参考

## 配置文件位置与优先级

1. 远程配置（最低优先级）
2. `~/.config/opencode/opencode.json`（全局）
3. `$OPENCODE_CONFIG` 环境变量指定路径
4. 项目根目录 `opencode.json`
5. `.opencode/opencode.json`（项目级）
6. `$OPENCODE_CONFIG_CONTENT`（内联配置）
7. 受管配置目录（最高优先级）

变量替换：`{env:VAR_NAME}` 引用环境变量，`{file:path}` 引用文件内容。

## 模型配置

```json
{
  "model": "anthropic/claude-sonnet-4-20250514",
  "small_model": "provider/cheap-model",
  "default_agent": "build",
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}",
        "baseURL": "https://api.anthropic.com",
        "timeout": 600000,
        "setCacheKey": true
      }
    }
  },
  "disabled_providers": ["openai", "gemini"],
  "enabled_providers": ["anthropic"]
}
```

认证优先级：环境变量 > auth.json > 配置文件。

## 权限系统

- `allow` — 允许执行，不问询
- `ask` — 每次确认
- `deny` — 禁止执行

可配置范围：全局、按 Agent、按工具、按文件路径模式。

```json
{
  "permission": {
    "edit": "ask",
    "bash": "allow",
    "glob": "allow",
    "external_directory": ["/home/user/external-projects"]
  }
}
```

## 思考深度（Ctrl+T 切换）

通过变体机制在不同思考深度间切换，影响推理 Token 消耗。
