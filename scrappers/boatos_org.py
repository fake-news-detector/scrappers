import requests
from bs4 import BeautifulSoup
import unicodedata


def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')


def should_ignore_paragraph(p):
    return "Ps.:" in p or "PS:" in p or "PS.:" in p or "Se você quiser sugerir" in p


def scrape_hoax(url):
    soup = get_soup(url)

    paragraphs = [
        p.get_text() for p in soup.select('#content [style="color: #ff0000;"]')
    ]
    if len(paragraphs) == 0:
        paragraphs = [p.get_text() for p in soup.select('#content em')]

    paragraphs = ["" if should_ignore_paragraph(p) else p for p in paragraphs]

    hoax = " ".join(paragraphs)

    clean_hoax = unicodedata.normalize("NFKD", hoax)

    if not clean_hoax.strip():
        return None

    return clean_hoax


def find_links_from_search_page(url):
    soup = get_soup(url)
    links = [a['href'] for a in soup.select('.more-link')]

    return links


def save_hoax(hoax):
    payload = {'uuid': 'scrapper', 'content': hoax, 'category_id': 2}

    return requests.post(
        'https://api.fakenewsdetector.org/vote_by_content', json=payload)


if __name__ == "__main__":
    initial_page = 13
    final_page = 40
    print('Start scrapping boatos.org from page', initial_page, 'to',
          final_page)
    for page in range(initial_page, final_page):
        print('Scrapping page', page)
        links = find_links_from_search_page('http://www.boatos.org/page/' +
                                            str(page) + '?s=%23boato')
        print('> Found', len(links), 'links')

        for link in links:
            print('> Scrapping', link)
            hoax = scrape_hoax(link)
            if hoax and len(hoax) > 100:
                print('>> Saving hoax:', hoax[:60])
                result = save_hoax(hoax)
                print('>> Result:', result)
            else:
                print('>> No hoax text found. Skipping...')