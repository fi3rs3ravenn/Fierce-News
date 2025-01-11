import requests
from bs4 import BeautifulSoup

def parse_tengrinews_tech():
    url = "https://tengrinews.kz/tag/tech/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []

        for item in soup.select("div.content_main_item"):
            title_tag = item.select_one('span.content_main_item_title')
            title = title_tag.text.strip() if title_tag else 'No title'

            link_tag = item.select_one('a')
            link = "https://tengrinews.kz" + link_tag['href'] if link_tag else "No link"

            articles.append({
                'title':title,
                'url':link,
            })

        return articles
    else:
        print(f'error: {response.status_code}')
        return []
    
if __name__ == "__main__":
    tech_news = parse_tengrinews_tech()
    for news in tech_news:
        print(f"Title: {news['title']}\nLink: {news['url']}\n")

