import functions as func
import pickle
import json

def analyze_articles(file_name, output_file_name, sentences_number, classifier_model):
    classifier_model = pickle.load(open('models/en_' + classifier_model + '.pkl', 'rb'))
    result = []
    
    with open(file_name, 'r', encoding='utf-8') as file:
        articles_json = file.read()
        articles = json.loads(articles_json)        

        for article in articles:
            text_from_url = func.fetch_data(article['url'])
            if text_from_url != None:
                text_summary, text_category = func.summarize_category(text_from_url, sentences_number, classifier_model)
            
                result.append({'title': article['title'],
                               'summary': text_summary,
                               'category': text_category,
                               'url': article['url']})
                
    with open(output_file_name, 'w', encoding='utf-8') as file:
        file.write(json.dumps(result, indent=4, ensure_ascii=False))
