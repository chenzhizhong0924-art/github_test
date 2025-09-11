import os
from flask import Flask, render_template, request, session, jsonify
from Rag import rag
import datetime

app = Flask(
    __name__,
    template_folder=os.path.join("web", "templates"),
    static_folder=os.path.join("web", "static")
)

app.secret_key = os.urandom(32)

SAVE_FOLDER = "logs"
os.makedirs(SAVE_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []
    if session.get("chat_history"):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(SAVE_FOLDER, f"{timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            for msg in session["chat_history"]:
                role = "使用者" if msg["role"] == "user" else "智能客服"
                f.write(f"{role}：{msg['text']}\n")
        session["chat_history"] = []
        session.modified = True

    return render_template("index.html", chat_history=[])


@app.route("/send_message", methods=["POST"])
def send_message():
    if "chat_history" not in session:
        session["chat_history"] = []

    data = request.get_json()
    user_message = data.get("message", "")
    rag_reply = rag.Rag(user_message)

    session["chat_history"].append({"role": "user", "text": user_message})
    session["chat_history"].append({"role": "gpt_text", "text": rag_reply})
    session.modified = True

    return jsonify({"reply": rag_reply})

@app.route("/save_chat", methods=["POST"])
def save_chat():
    data = request.get_json()
    messages = data.get("chat_history", [])

    if messages:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(SAVE_FOLDER, f"{timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            for msg in messages:
                role = "使用者" if msg["role"] == "user" else "智能客服"
                f.write(f"{role}：{msg['text']}\n")
    return jsonify({"status": "saved"})

if __name__ == "__main__":
    app.run(debug=True)