import requests
from bs4 import BeautifulSoup
import unicodedata
from multiprocessing import Pool
import pandas as pd

site = "hablillas.org"  # "boatos.org"
search_query = '?s=%23rumor'  # '?s=%23boato'


def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')


def should_ignore_paragraph(child):
    parent = child.parent
    if parent.name != 'p':
        parent = parent.parent
    p = parent.get_text()
    return ("Ps.:" in p or "PS:" in p or "PS.:" in p or "Se você quiser sugerir" in p or
            "Usted puede sugerir" in p or "Este artículo fue una sugerencia" in p)


def scrape_hoax(link):
    print('> Scrapping', link)
    soup = get_soup(link)

    paragraphs = [
        p.get_text() for p in soup.select('#content [style="color: #ff0000;"]')
    ]
    if len(paragraphs) == 0:
        paragraphs = [p.get_text()
                      if not should_ignore_paragraph(p) else ""
                      for p in soup.select('#content em')]

    hoax = " ".join(paragraphs)

    clean_hoax = unicodedata.normalize("NFKD", hoax).strip()

    time = soup.select_one('time[datetime]')
    timestamp = pd.to_datetime(time['datetime'])

    return {'link': link, 'timestamp': timestamp, 'hoax': clean_hoax}


def find_links_from_search_page(url):
    soup = get_soup(url)
    links = [a['href'] for a in soup.select('.more-link')]

    return links


def scrape_search_for_links(page_index):
    print('Scrapping page', page_index)
    links = find_links_from_search_page('http://www.' + site + '/page/' +
                                        str(page_index) + search_query)
    print('> Found', len(links), 'links for page', page_index)
    return links


if __name__ == "__main__":
    initial_page = 1
    final_page = 8  # 97
    print('Start scrapping', site, 'from page', initial_page, 'to',
          final_page)
    with Pool(5) as p:
        all_links = p.map(scrape_search_for_links,
                          range(initial_page, final_page))
        all_links = [val for sublist in all_links for val in sublist]
        print('> Found', len(all_links), 'total')

        all_hoaxes = p.map(scrape_hoax, all_links)

        df = pd.DataFrame(all_hoaxes)
        df = df[df['hoax'].str.len() > 100]
        df.to_csv(site + ".csv")
