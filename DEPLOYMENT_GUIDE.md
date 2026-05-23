# 每日心情笔记 - 部署指南

这个版本默认使用 Flask + Gunicorn 部署，推荐部署到 Render、Railway 或其他支持 Python Web Service 的平台。

## 必填配置

安装依赖：

```bash
pip install -r requirements.txt
```

启动命令：

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

`Procfile` 可以保持：

```text
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

## 推荐环境变量

```text
JSONBIN_API_KEY=你的 JSONBin API Key
JSONBIN_BIN_ID=你的 Bin ID
MOOD_PASSWORD=访问密码，可选但推荐
FLASK_DEBUG=0
```

如果没有配置 `JSONBIN_API_KEY` 和 `JSONBIN_BIN_ID`，应用会回退到内存存储。内存存储只适合测试，Render 免费实例重启后记录会丢失。

## JSONBin 数据格式

新版后端会保存为：

```json
{
  "notes": [
    {
      "id": 1770000000000,
      "mood": "开心+🥹",
      "text": "今天想说的话",
      "sender": "匿名",
      "tags": [],
      "reactions": {
        "抱抱你": 0,
        "收到啦": 0,
        "想你了": 0
      },
      "time": "2026-05-23T00:00:00Z"
    }
  ],
  "updated_at": "2026-05-23T00:00:00Z"
}
```

同时兼容旧版直接保存数组、旧记录没有 `reactions` 字段的格式，所以已有数据不需要手动迁移。

## API

- `GET /api/notes`：获取所有心情记录
- `POST /api/notes`：新增记录，`mood` 支持文字心情和表情心情，多个值用逗号分隔
- `POST /api/notes/<id>/reactions`：给记录增加回应，只支持 `抱抱你`、`收到啦`、`想你了`
- `DELETE /api/notes/<id>`：删除记录
- `GET /api/stats`：获取统计数据
- `GET /health`：健康检查

如果设置了 `MOOD_PASSWORD`，前端会先要求输入密码，API 请求需要携带：

```text
X-Mood-Password: 你的访问密码
```

## 本次改进点

- 增加表情心情：😋 🥲 🥹 🧐 🤓 😜 😝 😞 😟 😣 😖 ☹️ 😓 😱 😨 😰。
- 增加亲密回应按钮：抱抱你、收到啦、想你了。
- 旧数据自动补齐 `reactions`，无需手动迁移。
- 继续使用 JSONBin 持久化，Render 重启后记录不会丢失。
