import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

line_bot_sdk = LineBotApi(os.getenv("hCtBuU/rokYdDTqWbLoodMYntmrpqQcqtj7QC2maGvLqBd7W7VTrQtHOoZTqFqRdFeG6ALYq3EM0ypnpiFwh3lB4OTCIuS4cLZpqB0WSvdJWgNJGHenPyZZjb+tAmAdvh3lUrxQ4lrJLN0L5cRdgHAdB04t89/1O/w1cDnyilFU="))
handler = WebhookHandler(os.getenv("c4543b8cfd7cde163e7fd52c44695630"))

@app.route("/ callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    print(f"Received message from user ID: {user_id}")
    # ここでユーザーIDを使って何か処理できます
    reply_text = f"こんにちは！あなたのユーザーIDは {user_id} です。"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT",  5000)))
