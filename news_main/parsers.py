import requests
from bs4 import BeautifulSoup
from .models import News
from datetime import datetime
from dateutil import parser

def parse_habr_news():
    base_url = 'https://habr.com'
    url = f'{base_url}/ru/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')

    for article in articles:
        title_tag = article.find('a', class_='tm-title__link') # <a></a>
        if title_tag:
            title = title_tag.text.strip()  # .find('span')
            link = base_url + title_tag['href']
        else:
            continue

        description = 'no desc'
        try:
            article_response = requests.get(link)
            article_soup = BeautifulSoup(article_response.content, 'html.parser')

            description_div = article_soup.find('div', class_='article-formatted-body article-formatted-body article-formatted-body_version-2')
            if description_div:
                par = description_div.find_all('p')
                description = ' '.join(p.text.strip() for p in par if p.text)

            time_tag = article_soup.find('time')
            if time_tag and time_tag.has_attr('datetime'):
                published_date = parser.isoparse(time_tag['datetime'])
        except Exception as e:
            print(f'error while loading {link}: {e}')

            
        print(f'Adding news: {title[:10]}')
        print(f'Desc: {description[:15]}')
        print(f'datetime: {published_date}')

        if not News.objects.filter(title=title).exists():
            print(f'have detected:{title}')
            News.objects.create(
                title=title,
                link=link,
                description=description,
                source='Habr',
                published_date=published_date
            )
        else:
            print(f'already have: {title}')


