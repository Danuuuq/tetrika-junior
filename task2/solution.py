import asyncio
import aiohttp
from bs4 import BeautifulSoup
from collections import defaultdict
import re

BASE_URL = "https://ru.wikipedia.org"
CATEGORY_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"

async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_letter_page(session, url, letter, counter):
    while url:
        html = await fetch_html(session, url)
        soup = BeautifulSoup(html, "html.parser")

        for li in soup.select("#mw-pages li"):
            counter[letter] += 1

        next_link = soup.find("a", string="Следующая страница")
        if next_link:
            url = BASE_URL + next_link.get("href")
        else:
            url = None

async def parse_main_category():
    counter = defaultdict(int)

    async with aiohttp.ClientSession() as session:
        html = await fetch_html(session, CATEGORY_URL)
        breakpoint()
        soup = BeautifulSoup(html, "html.parser")

        tasks = []

        for link in soup.select("#mw-subcategories a"):
            title = link.text.strip()
            match = re.match(r"Животные, начинающиеся на «(.+)»", title)
            if match:
                letter = match.group(1)
                href = link["href"]
                url = BASE_URL + href
                tasks.append(parse_letter_page(session, url, letter, counter))

        await asyncio.gather(*tasks)

    return counter

async def main():
    counter = await parse_main_category()
    with open("animals_by_letter.csv", "w", encoding="utf-8") as f:
        for letter in sorted(counter):
            f.write(f"{letter},{counter[letter]}\n")
    # for letter in sorted(counter):
    #     print(f"{letter},{counter[letter]}")

if __name__ == "__main__":
    asyncio.run(main())
