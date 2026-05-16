"""
每日心情笔记 - Flask 后端
部署方式：Render / Railway / PythonAnywhere 等免费平台
"""
import os
import json
import threading
from datetime import datetime
from flask import Flask, request, jsonify, render_template, abort

app = Flask(__name__)

# ===== 配置 =====
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes.json")
# 设置访问密码（部署前请修改！留空则不需要密码）
ACCESS_PASSWORD = os.environ.get("MOOD_PASSWORD", "")

data_lock = threading.Lock()


def load_notes():
    """从 JSON 文件加载心情记录"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_notes(notes):
    """保存心情记录到 JSON 文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


# ===== 页面路由 =====

@app.route("/")
def index():
    """首页 — 心情笔记页面"""
    needs_password = bool(ACCESS_PASSWORD)
    return render_template("index.html", needs_password=needs_password)


@app.route("/login", methods=["POST"])
def login():
    """密码验证接口"""
    if not ACCESS_PASSWORD:
        return jsonify({"ok": True})

    data = request.get_json(silent=True) or {}
    if data.get("password") == ACCESS_PASSWORD:
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "密码不正确"}), 403


# ===== API 接口 =====

def check_auth():
    """检查密码验证（从 Header 中读取）"""
    if not ACCESS_PASSWORD:
        return True
    auth = request.headers.get("X-Mood-Password", "")
    return auth == ACCESS_PASSWORD


@app.route("/api/notes", methods=["GET"])
def api_get_notes():
    """获取所有心情记录"""
    if not check_auth():
        return jsonify({"error": "需要密码验证"}), 401

    with data_lock:
        notes = load_notes()
    return jsonify(notes)


@app.route("/api/notes", methods=["POST"])
def api_create_note():
    """创建一条心情记录"""
    if not check_auth():
        return jsonify({"error": "需要密码验证"}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "请求数据格式错误"}), 400

    mood = data.get("mood", "").strip()
    text = data.get("text", "").strip()

    if not mood:
        return jsonify({"error": "请选择一种心情"}), 400
    if not text:
        return jsonify({"error": "请写几句话"}), 400
    if len(text) > 500:
        return jsonify({"error": "内容不能超过 500 字"}), 400

    valid_moods = ["开心", "难过", "生气", "委屈", "想你", "需要安慰", "想一个人静静"]
    if mood not in valid_moods:
        return jsonify({"error": "心情类型无效"}), 400

    note = {
        "id": int(datetime.utcnow().timestamp() * 1000),
        "mood": mood,
        "text": text,
        "time": datetime.utcnow().isoformat() + "Z",
    }

    with data_lock:
        notes = load_notes()
        notes.insert(0, note)
        save_notes(notes)

    return jsonify(note), 201


@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def api_delete_note(note_id):
    """删除一条心情记录"""
    if not check_auth():
        return jsonify({"error": "需要密码验证"}), 401

    with data_lock:
        notes = load_notes()
        original_len = len(notes)
        notes = [n for n in notes if n["id"] != note_id]
        if len(notes) == original_len:
            return jsonify({"error": "记录不存在"}), 404
        save_notes(notes)

    return jsonify({"ok": True})


# ===== 健康检查 =====
@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat() + "Z"})


# ===== 启动 =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
