from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def get_asaminami_addresses():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    url = 'https://9db.jp/dqwalk/data/748?pref=広島県'
    driver.get(url)
    time.sleep(3)  # ページ読み込み待ち

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # ターゲット画像名の一部（末尾のパラメータ無視）
    target_img_filename = "img15350_1.jpg"

    # 画像要素をすべて検索（srcに部分一致するもの）
    matched_imgs = soup.find_all("img", class_=["wiki_monster", "wiki_kokoro1"])

    results = []

    for img in matched_imgs:
        src = img.get("src", "")
        if target_img_filename in src:
            mb4_div = img.find_parent("td")  # td → 中に mb4 が含まれている
            if mb4_div:
                mb4_content = mb4_div.find("div", class_="mb4")
                if mb4_content and "安佐南区" in mb4_content.text:
                    results.append(mb4_content.text.strip())

    return results

@app.route('/')
def index():
    addresses = get_asaminami_addresses()
    return render_template("index.html", addresses=addresses)

if __name__ == '__main__':
    app.run(debug=True)
