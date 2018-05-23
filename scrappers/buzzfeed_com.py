import requests
from bs4 import BeautifulSoup
import unicodedata
import os
import pandas as pd
from multiprocessing import Pool


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


def scrape_all_pages(category):
    initial_page = 1
    final_page = 50
    category_titles = []

    print('Scrapping category', category)
    for page in range(initial_page, final_page):
        print('Scrapping page', page)
        try:
            titles = find_titles_from_category_page(category, page)
            category_titles += titles
        except requests.exceptions.HTTPError:
            print('Page %s not found' % page)
            break

    return category_titles


def find_timestamp_for_post(item):
    index, post = item
    print("Finding timestamp for post %s" % (index + 1))
    soup = get_soup(post['url'])
    time = soup.select_one('[data-unix]')
    post['timestamp'] = pd.to_datetime(time['data-unix'], unit='s')

    return post


def add_timestamp_to_posts(posts):
    with Pool(5) as p:
        return p.map(find_timestamp_for_post, enumerate(posts))


if __name__ == "__main__":
    all_titles = []
    for category in ['lol', 'wtf', 'omg', 'cute']:
        category_titles = scrape_all_pages(category)
        all_titles += category_titles
    all_titles = add_timestamp_to_posts(all_titles)
    df = pd.DataFrame(all_titles)
    df.to_csv("clickbait_titles.csv")

    news_titles = scrape_all_pages("newsbr", "non_clickbait_titles.csv")
    news_titles = add_timestamp_to_posts(news_titles)
    df = pd.DataFrame(news_titles)
    df.to_csv("non_clickbait_titles.csv")
