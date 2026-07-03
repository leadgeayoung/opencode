# MCP 集成

MCP (Model Context Protocol) 是连接外部服务的标准协议。

## 配置方式

在 `opencode.json` 的 `mcpServers` 字段配置：

```json
{
  "mcpServers": {
    "my-service": {
      "command": "node",
      "args": ["path/to/server.mjs"],
      "env": {
        "API_KEY": "{env:MY_API_KEY}"
      }
    }
  }
}
```

## 类型

- **本地 MCP**：通过 command/args 启动子进程
- **远程 MCP**：通过 HTTP/SSE 连接外部服务

## 示例

MCP 图片生成、数据库查询、浏览器控制（Chrome DevTools）等。MCP 服务器可作为自定义工具供 AI 调用。
