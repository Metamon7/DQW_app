from bs4 import BeautifulSoup
import requests

url = 'https://9db.jp/dqwalk/data/748?pref=広島県'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# 絞り込み対象
target_src = "https://cdn08.net/dqwalk/data/img15/img15350_1.jpg?w=80"

# 条件：クラスに "wiki_monster" と "wiki_kokoro1" を含む & src が一致
images = soup.find_all("img", {
    "class": ["wiki_monster", "wiki_kokoro1"]
})

# srcが一致するものだけに絞る
filtered = [img for img in images if img.get("src") == target_src]

# 結果を表示
for img in filtered:
    print("対象画像が見つかりました！")
    print(f"src: {img.get('src')}")
