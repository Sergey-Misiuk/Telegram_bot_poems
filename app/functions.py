from bs4 import BeautifulSoup
import requests
from random import randint

from app.database.models import Poem


async def parser_poetry():
    source = "https://www.culture.ru/literature/poems"
    source_domain = "https://www.culture.ru"
    response = requests.get(source)
    html = BeautifulSoup(response.text, "lxml")
    qty_pages = html.find("div", class_="W6UA5").find_all("a")
    random_page = randint(1, int(qty_pages[2].get_text()))
    url = f"https://www.culture.ru/literature/poems?page={random_page}"
    response = requests.get(url)
    html = BeautifulSoup(response.text, "lxml")
    poem_links = html.find_all("div", class_="Dx0ke")
    random_poem = randint(0, len(poem_links) - 1)
    poem_link = poem_links[random_poem].find("a", class_="ICocV").get("href")
    url = f"{source_domain}{poem_link}"
    response = requests.get(url)
    html = BeautifulSoup(response.text, "lxml")
    author = html.select_one("div.HjkFX").get_text()
    poem_name = html.select_one("div.rrWFt").get_text()
    poem_paragraphs = html.select("div.xZmPc")
    poem_text = []
    for paragraph in poem_paragraphs[0]:
        if paragraph and str(paragraph).startswith(
            '<div class="" data-content="text"><br/><em>Читать'
        ):
            poem_text.append("")
            continue
        poem_text.append(
            str(paragraph)
            .replace(f'<div class="VKUQz" data-author-title="{author}">', "")
            .replace('<div class="JIu28">', "")
            .replace('<div class="" data-content="text">', "")
            .replace('<div class="WDqPo">', "")
            .replace("<!-- -->", "")
            .replace("</div>", "")
            .replace("<br/>", "\n")
            .replace("<p>", "")
            .replace("</p>", "")
        )
    poem_text = "\n\n".join(poem_text)
    return Poem(author=author, title=poem_name, text=poem_text)
