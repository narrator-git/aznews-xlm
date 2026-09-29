import json, httpx, time
from pathlib import Path
from bs4 import BeautifulSoup

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"
    )
}

CATEGORIES = {
    "sports": "https://apa.az/sport/football",
    "politics": "https://apa.az/politic",
    "economy": "https://apa.az/economy",
    "culture": "https://apa.az/culture",
    "world": "https://apa.az/world",
}

ARTICLES_PER_TOPIC = 10
out_path = Path("data/raw/apa.jsonl")
out_path.parent.mkdir(parents=True, exist_ok=True)
with out_path.open("w", encoding="utf-8") as f:
    for label, url in CATEGORIES.items():
        response = httpx.get(url, headers=headers, timeout=60, follow_redirects=True)
        soup = BeautifulSoup(response.text, "html.parser")
        urls=[]
        for card in soup.select("a.item"):
            href = (card.get("href") or "").strip()
            if href.startswith("https://apa.az/") and href.rsplit("-", 1)[-1].isdigit(): urls.append(href)
        print(label, "list", response.status_code, len(urls))

        for article_url in urls[:ARTICLES_PER_TOPIC]:
            time.sleep(1.5)
            article_resp=httpx.get(article_url, headers=headers, timeout=60, follow_redirects=True)
            if article_resp.status_code != 200:
                print("Skipping", article_resp.status_code, article_url)
                continue

            article = BeautifulSoup(article_resp.text, "html.parser")
            title = article.select_one("h2.title_news")
            date = article.select_one("div.date_news span.date")
            body = article.select_one("div.news_content")
            if (title is None) or (body is None):
                print("Skipping empty", article_url)
                continue

            article_row = {
                "url": article_url,
                "title": title.get_text(strip=True),
                "text": body.get_text(" ", strip=True),
                "date": date.get_text(strip=True) if date else None,
                "source": "apa.az",
                "label": label,
            }
            f.write(json.dumps(article_row, ensure_ascii=False) + "\n")
            print("Category:", label, "Article:", article_row["title"])
        time.sleep(2)