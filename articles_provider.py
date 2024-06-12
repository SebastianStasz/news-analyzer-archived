from substack_api import newsletter
import json


# categories = newsletter.list_all_categories()

def get_latest_articles():
    latest_articles = newsletter.get_newsletter_post_metadata("platformer", start_offset=0, end_offset=100)
    articles = []

    for article in latest_articles:
        articles.append({'title': article['title'],
                         'url': article['canonical_url']})

    with open('latest_articles.js', 'w', encoding='utf-8') as file:
        file.write(json.dumps(articles, indent=4, ensure_ascii=False))
