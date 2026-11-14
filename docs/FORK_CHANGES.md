# Fork 改动说明

本仓库基于 can4hou6joeng4/boss-agent-cli，保留上游历史、署名及 MIT 许可证。

## 新增功能

- `boss reply UID_OR_SECURITY_ID MESSAGE`：通过已登录的求职者聊天页发送后续消息。
- `--dry-run`：只解析联系人、预览目标和消息，不发送。
- 聊天页识别兼容 `/web/chat/index` 和 `/web/geek/chat`。

```sh
boss reply <联系人UID或securityId> "您好，想进一步了解这个岗位。" --dry-run
boss reply <联系人UID或securityId> "您好，想进一步了解这个岗位。"
```

发送时需要可通过 CDP 连接的 Chromium 浏览器，已登录 BOSS 并打开求职者聊天页，目标联系人须已加载。登录和浏览器配置沿用上游说明。

## 当前限制

该实现依赖网页内部 Vue 组件，页面升级可能造成兼容问题。当前 `ok` 返回值表示已调用页面发送逻辑，不代表服务端送达；发送后应查看当前会话确认结果，避免盲目重试导致重复消息。

上层批量投递脚本、个人简历、聊天记录、登录 Cookie、浏览器用户目录及投递日志不属于本次发布内容。该 Fork 不包含账号登录态，也不会自动回复招聘者。
