from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, PushMessageRequest, TextMessage
import time
import datetime

# LINE Botのアクセストークン
LINE_CHANNEL_ACCESS_TOKEN = 'hCtBuU/rokYdDTqWbLoodMYntmrpqQcqtj7QC2maGvLqBd7W7VTrQtHOoZTqFqRdFeG6ALYq3EM0ypnpiFwh3lB4OTCIuS4cLZpqB0WSvdJWgNJGHenPyZZjb+tAmAdvh3lUrxQ4lrJLN0L5cRdgHAdB04t89/1O/w1cDnyilFU='
USER_ID = 'huntershu-'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def get_asaminami_addresses():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    url = 'https://9db.jp/dqwalk/data/748?pref=広島県'
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    target_img_filename = "img15350_1.jpg"
    matched_imgs = soup.find_all("img", class_=["wiki_monster", "wiki_kokoro1"])

    results = []
    for img in matched_imgs:
        src = img.get("src", "")
        if target_img_filename in src:
            parent_td = img.find_parent("td")
            if parent_td:
                mb4_div = parent_td.find("div", class_="mb4")
                if mb4_div and "安佐南区" in mb4_div.text:
                    results.append(mb4_div.text.strip())
    return results

def send_line_message(text):
    # 設定
    configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)

        # メッセージ構築
        message = TextMessage(text=text)
        request = PushMessageRequest(to=USER_ID, messages=[message])

        # メッセージ送信
        messaging_api.push_message(push_message_request=request)

def job():
    print(f"[{datetime.datetime.now()}] 情報取得・送信中")
    addresses = get_asaminami_addresses()
    if addresses:
        message = "スライムプディング（img15350_1）が出現！\n" + "\n".join(f"{i+1}. {a}" for i, a in enumerate(addresses))
    else:
        message = "安佐南区にスライムプディングの出現はありませんでした。"

    send_line_message(message)

# スケジュール設定
scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', hour=12, minute=0)
scheduler.add_job(job, 'cron', hour=15, minute=0)

# 起動時に1回実行
job()
scheduler.start()
