import requests
from bs4 import BeautifulSoup
import unicodedata

def scrape_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    paragraphs = [p.get_text() for p in
                  soup.select('#content [style="color: #ff0000;"]')]
    if len(paragraphs) == 0:
        paragraphs = [p.get_text() for p in
                      soup.select('#content em')]

    paragraphs = ["" if "Ps.:" in p else p for p in paragraphs]

    hoax = " ".join(paragraphs)

    clean_hoax = unicodedata.normalize("NFKD", hoax)

    if not clean_hoax.strip():
        return None

    return clean_hoax
