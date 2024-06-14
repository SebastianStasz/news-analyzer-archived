from articles_provider import get_latest_news_articles
from articles_analyzer import analyze_articles
from results_analyzer import analyze_results

models = ['ridge_model', 'random_forest_model', 'logistic_regression_model', 'kneighbors_model', 'gaussian_nb_model', 'decision_tree_model']

if __name__ == '__main__':
    print('Start')
    analyze_results('latest_news_articles_summary.js')
    
    # sentences_number = 10
    # model_name = 'ridge_model'
    # analyze_articles('latest_news_articles.js', 'latest_news_articles_summary.js', sentences_number, model_name)

    # get_latest_news_articles()
