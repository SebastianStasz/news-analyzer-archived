from articles_provider import get_latest_articles
from articles_analyzer import analyze_articles

models = ['ridge_model', 'random_forest_model', 'logistic_regression_model', 'kneighbors_model', 'gaussian_nb_model', 'decision_tree_model']

if __name__ == '__main__':
    sentences_number = 10
    model_name = 'ridge_model'
    analyze_articles('latest_articles.js', 'latest_articles_summary.js', sentences_number, model_name)
