import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_tengrinews_article(article_url):
    response = requests.get(article_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # content_main_inner -> content_main_text
        content_inner = soup.select_one("div.content_main_inner")
        if content_inner:
            content_text = content_inner.select_one("div.content_main_text")
            if content_text:
                paragraphs = content_text.find_all("p")
                full_text = "\n".join([p.text.strip() for p in paragraphs])
                return full_text
            else:
                return "no text"
        else:
            return "No content_main_inner"
    else:
        return f"Error {response.status_code}"

def parse_tengrinews():
    base_url = "https://tengrinews.kz"
    url = f"{base_url}/tag/tech/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []

        for item in soup.select("div.content_main_item"):
            title_tag = item.select_one('span.content_main_item_title')
            title = title_tag.text.strip() if title_tag else 'No title'
            link_tag = item.select_one('a')
            link = urljoin(base_url, link_tag['href']) if link_tag else "No link"

            if link:
                full_text = parse_tengrinews_article(link)

                articles.append({
                    'title': title,
                    'url': link,
                    'description': full_text,
                })

        return articles
    else:
        print(f'error: {response.status_code}')
        return []

if __name__ == "__main__":
    tech_news = parse_tengrinews()
    for news in tech_news:
        print(f"Title: {news['title']}\nLink: {news['url']}\nDescription:\n{news['description']}\n{'-'*80}\n")
