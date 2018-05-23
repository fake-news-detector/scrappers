import requests
from bs4 import BeautifulSoup
import unicodedata
import os


def get_soup(url):
    page = requests.get(url)
    page.raise_for_status()
    return BeautifulSoup(page.text, 'html.parser')


def find_titles_from_category_page(category, page):
    soup = get_soup('https://www.buzzfeed.com/br/feedpage/feed/search_buzzes?page=' +
                    str(page) + '&page_name=badge&tags.tag_name=' + category)
    titles = [{'title': h2.text,
               'url': 'https://www.buzzfeed.com' + h2.parent['href']}
              for h2 in soup.select('h2')]

    return titles


def append_to_csv(filename, items):
    head = ""
    if not os.path.exists(filename):
        head = ",".join(items[0].keys())

    with open(filename, "a") as myfile:
        lines = [",".join(item.values()) for item in items]
        myfile.write(head + "\n" + "\n".join(lines))


def scrape_all_pages(category, filename):
    initial_page = 1
    final_page = 50

    print('Scrapping category', category)
    for page in range(initial_page, final_page):
        print('Scrapping page', page)
        try:
            titles = find_titles_from_category_page(category, page)
            append_to_csv(filename, titles)
        except requests.exceptions.HTTPError:
            print('Page %s not found' % page)
            break


if __name__ == "__main__":
    for category in ['lol', 'wtf', 'omg', 'cute']:
        scrape_all_pages(category, "clickbait_titles.csv")

    scrape_all_pages("newsbr", "non_clickbait_titles.csv")
