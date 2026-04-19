from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELETYPE_API_URL = "https://api.teletype.app/public/api/v1/message/send"
TELETYPE_TOKEN = os.getenv("TELETYPE_TOKEN", "ВАШ_TOKEN_СЮДА")
DIALOG_ID = os.getenv("TELETYPE_DIALOG_ID", "ВАШ_DIALOG_ID_СЮДА")

@app.route("/alert", methods=["POST"])
def alert():
    try:
        payload = request.get_json(force=True)
    except Exception:
        return "Invalid JSON", 400

    status = payload.get("status", "unknown")
    title = payload.get("title", "Алерт")
    
    # Формируем читаемый текст
    text = f"⚠️ Статус: {status.upper()}\n📢 Группа: {title}\n\n"
    
    for a in payload.get("alerts", []):
        labels = a.get("labels", {})
        alertname = labels.get("alertname", "Без имени")
        instance = labels.get("instance", "")
        text += f"• {alertname} ({instance})\n"

    # Отправка в Teletype (используем files={}, чтобы Content-Type стал multipart/form-data)
    headers = {
        "X-Auth-Token": TELETYPE_TOKEN,
        "accept": "application/json"
    }
    
    files = {
        "dialogId": (None, DIALOG_ID),
        "text": (None, text)
    }

    try:
        resp = requests.post(TELETYPE_API_URL, headers=headers, files=files, timeout=10)
        if resp.ok:
            return "OK", 200
        else:
            return f"Teletype error: {resp.status_code} {resp.text}", 502
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    # Запускаем на всех интерфейсах (0.0.0.0) и порту 5050
    app.run(host="0.0.0.0", port=5050)
