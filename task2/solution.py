import asyncio
import aiohttp
from bs4 import BeautifulSoup
from collections import defaultdict
import re

BASE_URL = "https://ru.wikipedia.org"
CATEGORY_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"
RUSSIAN_LETTER_PATTERN = re.compile(r'^[А-ЯЁ]$', re.IGNORECASE)

async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_main_category():
    counter = defaultdict(int)
    counter['letter'] = 'count'

    async with aiohttp.ClientSession() as session:
        url = CATEGORY_URL
        while url:
            html = await fetch_html(session, url)
            soup = BeautifulSoup(html, "html.parser")
            header = soup.find(id='mw-pages')
            next_page = header.find('a', string='Следующая страница')
            categories = header.find_all('div', attrs={'class': 'mw-category-group'})
            for category in categories:
                letter = category.find('h3').text
                if not RUSSIAN_LETTER_PATTERN.match(letter):
                    next_page = None
                    break
                counter[letter] += len(category.find_all('a'))
            url = BASE_URL + next_page.get('href') if next_page else None
    return counter

async def main():
    counter = await parse_main_category()
    with open("animals_by_letter.csv", "w", encoding="utf-8") as f:
        for letter in sorted(counter):
            f.write(f"{letter},{counter[letter]}\n")

if __name__ == "__main__":
    asyncio.run(main())
