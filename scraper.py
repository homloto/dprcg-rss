import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

URL = "https://dprcg.gov.in/news/district-news"

fg = FeedGenerator()
fg.title("DPRCG News Feed")
fg.link(href="https://dprcg.gov.in")
fg.description("Auto generated DPRCG RSS Feed")

try:
    r = requests.get(
        URL,
        timeout=120,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
        }
    )

    print("Status Code:", r.status_code)
    print("Page Length:", len(r.text))
    print(r.text[:1000])

    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.find_all("a")

    print("Total Links Found:", len(links))

    count = 0

    for a in links:
        title = a.get_text(strip=True)
        href = a.get("href")

        if not title or not href:
            continue

        if not href.startswith("http"):
            href = "https://dprcg.gov.in" + href

        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=href)

        count += 1

        if count >= 30:
            break

except Exception as e:
    print("ERROR:", e)

fg.rss_file("dprcg.xml")
print("RSS generated")
