import requests
from bs4 import BeautifulSoup
import time
import random
import re
import pandas as pd


def get_sections(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # delfi.lt/en has sections: politics, business and ect.
    # to find articles on these pages, first collect all section urls
    menu_item_link = []
    for menu in soup.find_all('li', class_="C-header-menu__item"):
        menu_item_link.append("https://www.delfi.lt" + menu.find('a', class_="C-header-menu__item-content").get('href'))

    # only first 6 links are valid
    menu_item_link = menu_item_link[0:5]

    return menu_item_link


def get_section_links(menu_item_link):
    # define url's list of first 3 pages for each section,
    # if sections has <3 pages then retrieve all url's of this section
    url_final_list = []

    # loop over menu items (sections)
    for url_menu in menu_item_link:
        response_menu = requests.get(url_menu)
        soup_menu = BeautifulSoup(response_menu.content, 'html.parser')
        print(url_menu)

        # get the last page number
        buttons = soup_menu.find_all('button', class_='C-pagination__button', type="button")
        last_page = buttons[-2].get_text(strip=True)

        # check if the last page is <5
        last_page = int(last_page) if int(last_page) < 3 else 3

        # construct page links
        for page in range(1, last_page + 1):
            url_final_list.append(url_menu + "?page=" + str(page))

    return url_final_list


def get_articles(url_final_list):

    # get the articles headline, url and label
    articles = []

    # loop over all collected URL's
    for url in url_final_list:

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # loop over all headlines in a single page of a section
        for headline_block in soup.find_all(class_='C-block-type-102-headline__content'):

            # extract the headline text
            headline = headline_block.find('div', class_="C-block-type-102-headline__title")
            headline_text = headline.get_text(strip=True)
            # print(headline_text)

            # extract the URL
            headline_url = "www.delfi.lt" + headline.find('a', class_="").get('href')
            # print(headline_url)

            # Find the label of the article type
            article_label = headline_block.find('div',
                                                class_='C-headline-labels C-block-type-102-headline__labels')  # .find('a', class_="")
            # print(article_label)

            # check if article has label information
            if article_label:
                label_text = article_label.get_text(strip=True)
            else:
                label_text = 'No label found'
            # print(label_text)

            # store the data in a dictionary and append to the list
            articles.append({
                'headline': headline_text,
                'url': headline_url,
                'label': label_text
            })

        # print("Section: " + label_text + " | Page: ", re.search(r'page[/=](\d+)', url).group(1))
        # time.sleep(random.uniform(1, 5))

    print("Total articles found: " + str(len(articles)))
    return articles


if __name__ == "__main__":
    website = 'https://www.delfi.lt/en'
    sections = get_sections(website)
    section_links = get_section_links(sections)
    articles_info = get_articles(section_links)

    articles_pd = pd.DataFrame(articles_info)
    articles_pd.to_csv('article_data.csv', index=False, encoding='utf-8')
