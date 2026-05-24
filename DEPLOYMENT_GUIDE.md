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
DEFAULT_WEATHER_CITY=厦门海沧
DEEPSEEK_API_KEY=你的 DeepSeek API Key，可选
DEEPSEEK_MODEL=deepseek-chat
```

如果没有配置 `JSONBIN_API_KEY` 和 `JSONBIN_BIN_ID`，应用会回退到内存存储。内存存储只适合测试，Render 免费实例重启后记录会丢失。

如果没有配置 `DEEPSEEK_API_KEY`，智能分析会自动使用本地规则兜底，页面不会坏。

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
- `GET /api/weather?city=厦门海沧`：获取默认城市天气
- `GET /api/weather?lat=...&lon=...`：获取当前位置天气
- `GET /api/analysis`：获取小蜥蜴智能分析，优先 DeepSeek，失败时本地规则兜底
- `GET /health`：健康检查

如果设置了 `MOOD_PASSWORD`，前端会先要求输入密码，心情和分析 API 请求需要携带：

```text
X-Mood-Password: 你的访问密码
```

## 本次改进点

- 增加四款可切换主题：奶粉、夜紫、云蓝、草莓。
- 每款主题有独立配色和原创可爱背景元素，不使用官方版权角色素材。
- 增加天气预报卡片：默认厦门海沧，可手动授权使用当前位置。
- 增加智能分析提醒：配置 DeepSeek 后使用 AI；未配置时自动使用本地规则。
- 增加表情心情：😋 🥲 🥹 🧐 🤓 😜 😝 😞 😟 😣 😖 ☹️ 😓 😱 😨 😰。
- 增加亲密回应按钮：抱抱你、收到啦、想你了。
- 旧数据自动补齐 `reactions`，无需手动迁移。
- 继续使用 JSONBin 持久化，Render 重启后记录不会丢失。
