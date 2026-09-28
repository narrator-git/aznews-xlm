import json, httpx, time
from pathlib import Path 
from bs4 import BeautifulSoup

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"
    )
}

URL = "https://apa.az/sport/football"
response = httpx.get(URL, headers=headers, timeout=60, follow_redirects=True)
print("response status:", response)
soup = BeautifulSoup(response.text, "html.parser")

urls = []
for card in soup.select("a.item"):
    href = (card.get("href") or "").strip()
    if (href.startswith("https://apa.az/") and href.rsplit("-", 1)[-1].isdigit()): urls.append(href)
print("Found", len(urls), "urls!")

out_path = Path("data/raw/apa.jsonl")
out_path.parent.mkdir(parents=True, exist_ok=True)

with out_path.open("w", encoding="utf-8") as f:
    for article_url in urls[:10]:
        time.sleep(1.5)
        article_resp = httpx.get(article_url, headers=headers, timeout=60, follow_redirects=True)
        if article_resp.status_code != 200:
            print("Skipping ", article_resp.status_code, article_url)
            continue

        article = BeautifulSoup(article_resp.text, "html.parser")
        title = article.select_one("h2.title_news")
        date = article.select_one("div.date_news span.date")
        body = article.select_one("div.news_content")
        if title == None or body == None:
            print("Skipping empty", article_url)
            continue

        article_row = {
            "url": article_url,
            "title": title.get_text(strip=True),
            "text": body.get_text(" ", strip=True),
            "date": date.get_text(strip=True) if date else None,
            "source": "apa.az",
            "label": "sports",
        }
        f.write(json.dumps(article_row, ensure_ascii=False) + "\n")