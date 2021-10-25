import requests
import bs4
import re

response = requests.get('https://habr.com/ru/all/')
response.raise_for_status()

KEYWORDS = {'дизайн', 'фото', 'web', 'python'}

soup = bs4.BeautifulSoup(response.text, features='html.parser')
articles = soup.find_all('article')

for article in articles:
    hubs = article.find_all(class_="tm-article-snippet__hubs-item")
    hubs_set = set(hub.find('span').text for hub in hubs)

    title = article.find('h2').text
    title_list = re.findall("\w+", title)
    title_set = set(title.lower() for title in title_list)

    link = article.find(class_="tm-article-snippet__readmore").attrs['href']
    link_to_the_page = 'https://habr.com' + link

    text = article.find(class_="article-formatted-body article-formatted-body_version-2")
    if text is not None:
        response_text = requests.get(link_to_the_page)
        response_text.raise_for_status()
        soup = bs4.BeautifulSoup(response_text.text, features='html.parser')
        text_all = soup.find_all('article')
        for text in text_all:
            text_str = text.find(class_="article-formatted-body article-formatted-body_version-2").text
            text_list = re.findall("\w+", text_str)
            text_set = set(text.lower() for text in text_list)

    datetime = article.find(class_="tm-article-snippet__datetime-published")
    datetime = datetime.find('time').attrs['title']

    if KEYWORDS & title_set or KEYWORDS & hubs_set or KEYWORDS & text_set:
        print(f'{datetime} - {title} - {link_to_the_page}')
        print('_____')
