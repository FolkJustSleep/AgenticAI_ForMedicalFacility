import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
# print(f"Loaded LINE_CHANNEL_ACCESS_TOKEN: {ACCESS_TOKEN}")

def reply_message(reply_token: str, message: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    response = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=data)
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code} - {response.text}")