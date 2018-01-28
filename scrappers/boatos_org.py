import requests
from bs4 import BeautifulSoup
import unicodedata

def scrape_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    red_paragraphs = soup.select('#content [style="color: #ff0000;"]')

    hoax = [p.get_text() for p in red_paragraphs]
    hoax = "".join(hoax)

    clean_hoax = unicodedata.normalize("NFKD", hoax)

    return clean_hoax
