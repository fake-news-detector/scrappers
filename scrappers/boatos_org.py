import requests
from bs4 import BeautifulSoup
import unicodedata


def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')


def scrape_hoax(url):
    soup = get_soup(url)

    paragraphs = [
        p.get_text() for p in soup.select('#content [style="color: #ff0000;"]')
    ]
    if len(paragraphs) == 0:
        paragraphs = [p.get_text() for p in soup.select('#content em')]

    paragraphs = ["" if "Ps.:" in p else p for p in paragraphs]

    hoax = " ".join(paragraphs)

    clean_hoax = unicodedata.normalize("NFKD", hoax)

    if not clean_hoax.strip():
        return None

    return clean_hoax


def find_links_from_search_page(url):
    soup = get_soup(url)
    links = [a['href'] for a in soup.select('.more-link')]

    return links
