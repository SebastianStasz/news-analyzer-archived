import json
import matplotlib.pyplot as plt
from urllib.parse import urlparse
import re

def drawHorizontalChart(chart_name, file_name, data: dict):
    x_axis = data.keys()
    y_axis = data.values()
    plt.barh(range(len(data)),y_axis,tick_label=x_axis)
    plt.title(chart_name)
    plt.savefig(file_name,bbox_inches='tight',  dpi = 400)
    plt.show()

def analyze_results(file_name):
    domains_amount = {}
    categories_euronews = {}
    categories_amount = {}
    
    with open(file_name, 'r', encoding='utf-8') as file:
        articles_json = file.read()
        articles = json.loads(articles_json)        

    for article in articles:
        url = article['url']
        domain = urlparse(url).netloc
        category = article['category']

        if domain not in domains_amount:
            domains_amount.update({domain: 1})
        else:
            domains_amount[domain] += 1
        if category not in categories_amount:
            categories_amount.update({category: 1})
        else:
            categories_amount[category] += 1
        if domain == 'www.euronews.com' and category not in categories_euronews:
            categories_euronews.update({category: 1})
            print(domain)
        elif domain == 'www.euronews.com':
            print(domain + "ez")
            print(category)
            print(categories_euronews)
            categories_euronews[category] += 1
                     
    print(categories_euronews)

    # pattern = r"(www\.)?"
    # domains_amount_clean = {}
    # for domain in domains_amount:
    #     domain_clean = re.sub(pattern,'', domain)
    #     print(domain_clean)
    #     domains_amount_clean[domain_clean] = domains_amount[domain]

    drawHorizontalChart("Categories occurences", "categories_occurences.png", categories_amount)
