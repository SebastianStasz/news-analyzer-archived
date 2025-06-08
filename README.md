# News analyzer [Archived]

**news-analyzer** is a Python-based project designed for news article analysis. It provides functionality to fetch, analyze, and summarize articles from various sources. The project employs machine learning models and natural language processing (NLP) techniques to categorize articles and generate summaries. The system uses multiple modules to:
1. Fetch the latest news articles from an API.
2. Analyze the fetched articles using pre-trained machine learning models.
3. Summarize articles using NLP techniques.
4. Visualize results and article statistics.

## Key Features:
- Fetches the latest news articles using the **NewsDataApiClient**.
- Summarizes articles using an NLP-based summarizer.
- Categorizes articles using machine learning models (e.g., Ridge, Random Forest, Logistic Regression).
- Visualizes data and results through charts.

## Key Technologies:
- **Python** for programming.
- **Flask** for web framework (listed in `requirements.txt`).
- **Scikit-learn** for machine learning.
- **BeautifulSoup** and **requests** for web scraping.
- **NLTK** for natural language processing.
- **Matplotlib** for visualizations.
