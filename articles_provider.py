import json
from newsdataapi import NewsDataApiClient


# categories = newsletter.list_all_categories()

def get_latest_news_articles():
    api = NewsDataApiClient(apikey='')
    pages = 30
    articles = []
    next_page = None

    for page in range(pages):
        latest_articles = api.news_api(country='pl', language='en', page=next_page)
        print(f'Fetching articles for page: {page}')
        next_page = latest_articles['nextPage']
        
        for article in latest_articles['results']:
            if article['title'] in articles:
                continue
            
            articles.append({'title': article['title'],
                             'url': article['link']})
    
            with open('latest_news_articles.js', 'w', encoding='utf-8') as file:
                file.write(json.dumps(articles, indent=4, ensure_ascii=False))
