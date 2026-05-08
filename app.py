from flask import Flask, request
import requests
import os
from datetime import datetime
import pytz

# ================= CONFIG =================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")

# ================= TELEGRAM =================
def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except Exception as e:
        print("Telegram Error:", e)

# ================= TIME =================
def get_time():
    return datetime.now(IST).strftime("%H:%M %p")

# ================= WEBHOOK =================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    try:
        msg = f"""
📊 CPR STRATEGY ALERT

{data.get("signal")}
📈 Symbol: {data.get("symbol")}

🔹 CPR: {data.get("cpr")}
🔹 ROC: {data.get("roc")}
🔹 Trend: {data.get("trend")}

💰 Price: {data.get("price")}
⏰ Time: {get_time()}
"""
        send_telegram(msg)
        return "OK"

    except Exception as e:
        print("Webhook Error:", e)
        return "ERROR"

# ================= TEST ROUTE =================
@app.route("/")
def home():
    return "✅ Bot Running - Webhook Mode"

@app.route("/test")
def test():
    send_telegram("✅ Test Alert Working")
    return "Test Sent"

# ================= START =================
if __name__ == "__main__":
    print("🚀 Bot Started")
    app.run(host="0.0.0.0", port=10000)