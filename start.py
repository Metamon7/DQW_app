from flask import Flask, request
from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
from linebot.v3.webhook import MessageEvent
from linebot.v3.messaging.models import TextMessage
import json
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = 'hCtBuU/rokYdDTqWbLoodMYntmrpqQcqtj7QC2maGvLqBd7W7VTrQtHOoZTqFqRdFeG6ALYq3EM0ypnpiFwh3lB4OTCIuS4cLZpqB0WSvdJWgNJGHenPyZZjb+tAmAdvh3lUrxQ4lrJLN0L5cRdgHAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'c4543b8cfd7cde163e7fd52c44695630'

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    try:
        events = parser.parse(body, signature)
    except Exception as e:
        print("署名エラー:", e)
        return 'Signature Error', 400

    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)

        for event in events:
            if isinstance(event, MessageEvent):
                user_id = event.source.user_id
                print(f"[✅ USER_ID]: {user_id}")

                # 確認用メッセージを送る
                messaging_api.push_message(
                    push_message_request={
                        "to": user_id,
                        "messages": [{"type": "text", "text": f"あなたのIDは {user_id} です"}]
                    }
                )

    return 'OK', 200
