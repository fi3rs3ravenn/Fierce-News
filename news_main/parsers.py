import requests
from bs4 import BeautifulSoup
from .models import News
from dateutil import parser
from urllib.parse import urljoin
from django.utils import timezone
from fake_useragent import UserAgent
import time



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
            time.sleep(2)
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


MAX_RETIRES = 3
def make_request(url):
    ua = UserAgent()
    for i in range(MAX_RETIRES):
        try:
            headers = {'User-Agent': ua.random}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            print(f'Retry:{i+1}/{MAX_RETIRES} for {url}')
            time.sleep(2)
    return None



def parse_tengrinews():
    base_url = "https://tengrinews.kz"
    url = f"{base_url}/tag/tech/"
    response = make_request(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("div.content_main_item")
        print(f'found {len(articles)}')
        for item in articles:
            title_tag = item.select_one('span.content_main_item_title')
            title = title_tag.text.strip() if title_tag else 'No title'
            link_tag = item.select_one('a')
            link = urljoin(base_url, link_tag['href']) if link_tag else "No link"

            description = 'No Desc'
            try:
                article_response = requests.get(link)
                article_soup = BeautifulSoup(article_response.text, "html.parser")
                content_inner = article_soup.select_one("div.content_main_inner")
                if content_inner:
                    content_text = content_inner.select_one("div.content_main_text")
                    if content_text:
                        paragraphs = content_text.find_all("p")
                        description = "\n".join([p.text.strip() for p in paragraphs])
            except Exception as e:
                print(f"Error while loading: {e}")


 #solution for a while

            print(f'Adding news: {title[:10]}')
            print(f'Desc: {description[:15]}')

            if not News.objects.filter(title=title).exists():
                print(f'have detected:{title}')
                News.objects.create(
                    title=title,
                    link=link,
                    description=description,
                    source='TengriNews',
                    published_date=timezone.now()
                    )
            else:
                print(f'already have: {title}')
    else:
        print(f'error: {response.status_code}')


def run_all_parsers():
    print('Starting Habr news parcing...')
    parse_habr_news()

    print('Starting TengriNews parcing...')
    parse_tengrinews()