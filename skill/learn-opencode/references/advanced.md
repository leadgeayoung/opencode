# 进阶功能

## 主题系统

- 50+ 内置主题，通过 `/theme` 切换或在 `opencode.json` 中配置
- 需终端支持 truecolor：`echo $COLORTERM` 输出 `truecolor` 或 `24bit`

## 快捷键定制

在 `opencode.json` 的 `keybinds` 字段自定义，参见 `references/../6b-keybinds`。

## SDK 开发

TypeScript/JavaScript SDK（`@opencode-ai/plugin`），可编程控制 OpenCode：
- 创建会话、发送消息、监听事件
- 构建自定义工具和插件

## 自定义工具

`.opencode/tool/*.ts`，使用 `tool()` 辅助函数，类型安全验证。

## 插件系统

`.opencode/plugins/*.js`，支持 Hooks 机制（`12c-hooks.md`）。

## 远程模式

`opencode` 启动两个组件：
- HTTP 服务器（OpenAPI 3.1 REST API）
- TUI 客户端

支持多客户端同时连接、Web 界面、远程访问。

## 企业版

LDAP/SAML 认证、审计日志、统一管理，见 `11-enterprise.md`。
