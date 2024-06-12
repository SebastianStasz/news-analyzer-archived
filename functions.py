# Przygotowanie bibliotek i danych
import nltk
import re
import heapq
import pandas as pd
from string import punctuation
punctuation = punctuation + '\n'
from bs4 import BeautifulSoup
from urllib.request import urlopen
from nltk.stem.isri import ISRIStemmer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import requests

# Kategorie tekstów
categories = ['Economy & Business', 'Diverse News', 'Politic', 'Sport', 'Technology']

'''
Budowanie podsumowującego algorytmu
Funkcja nltk_summarizer jest używana do tworzenia streszczenia wejściowego tekstu, bazując na częstotliwości słów w tekście.

Funkcja zaczyna od połączenia listy stopwords (słów powszechnie pomijanych w analizie tekstu) z języka arabskiego i angielskiego i zapisania ich w zbiorze stopWords.

Następnie funkcja inicjalizuje pusty słownik word_frequencies do przechowywania częstotliwości występowania słów. 
Jeśli słowo nie jest stopword ani znakiem interpunkcyjnym, jest dodawane do word_frequencies lub jego częstotliwość jest zwiększana, jeśli już tam jest.

Funkcja znajduje maksymalną częstotliwość występowania słowa w word_frequencies.
Dla każdego słowa w word_frequencies, normalizuje jego częstotliwość przez podzielenie przez maksymalną częstotliwość.

Funkcja dzieli wejściowy tekst na listę zdań sentence_list.

Następnie oblicza punktację zdań.
Inicjalizuje pusty słownik sentence_scores do przechowywania punktacji zdań.
Dla każdego zdania w sentence_list -> Dla każdego słowa w zdaniu (po konwersji na małe litery i tokenizacji):
Jeśli słowo jest w word_frequencies, a długość zdania jest mniejsza niż 30 słów, punktacja zdania jest zwiększana o częstotliwość tego słowa.

Funkcja wybiera number_of_sentence zdań o najwyższych punktacjach za pomocą heapq.nlargest i zapisuje je w summary_sentences.
Na końcu tworzone jest streszczenie.

Łączy wybrane zdania w jeden ciąg tekstowy, tworząc streszczenie.
'''
def nltk_summarizer(input_text, number_of_sentence):
    stopWords = set(nltk.corpus.stopwords.words("english"))
    word_frequencies = {}
    for word in nltk.word_tokenize(input_text):
        if word not in stopWords:
            if word not in punctuation:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

    sentence_list = nltk.sent_tokenize(input_text)
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(number_of_sentence, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary

# Wczytywanie angielskiego zestawu danych
en_data = pd.read_csv(r"dataset/bbc_news_dataset.csv")
en_data = en_data.replace("entertainment", "diverse news")
en_data = en_data.replace("business", "economy & business")

# Sterylizacja danych
# Usuwanie linków:
# To usunie wszystkie linki z tekstu, w tym:
# Dopasowanie protokołów http, takich jak [**http:// lub https://**].
# Dopasowanie opcjonalnych białych znaków po protokołach http.
# Opcjonalnie dopasowanie włączenia [**www.**] lub nie.
# Opcjonalne dopasowanie białych znaków w linkach.
# Dopasowanie 0 lub więcej słów, zakończonych kropką.
# Dopasowanie 0 lub więcej słów (lub myślnika lub spacji) zakończonych [**\\**].
# Każda pozostała ścieżka na końcu url zakończona opcjonalnym zakończeniem.
# Dopasowanie końcowych parametrów zapytania (nawet z białymi znakami itp.).
def delete_links(input_text):
    pettern = r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))'''
    out_text = re.sub(pettern, ' ', input_text)
    return out_text

# Naprawianie wydłużania słów:
# Wydłużanie słów występuje, gdy znaki są błędnie powtarzane. Angielskie słowa mają maksymalnie dwa powtórzone znaki, jak w słowach [**wood, school**].
# Dodatkowe znaki muszą być usunięte, w przeciwnym razie możemy dodać mylące informacje.
def delete_repeated_characters(input_text):
    pattern = r'(.)\1{2,}'
    out_text = re.sub(pattern, r"\1\1", input_text)
    return out_text

# Zastępowanie specjalnych liter innymi
# W języku arabskim istnieje wiele liter, które można przekształcić w inne
def replace_letters(input_text):
    replace = {"أ": "ا", "ة": "ه", "إ": "ا", "آ": "ا", "": ""}
    replace = dict((re.escape(k), v) for k, v in replace.items())
    pattern = re.compile("|".join(replace.keys()))
    out_text = pattern.sub(lambda m: replace[re.escape(m.group(0))], input_text)
    return out_text

# Usuwanie złych symboli:
# Ta metoda usuwa niechciane znaki z tekstu, takie jak znaki zapytania, przecinki, gwiazdki, plusy itd.
def clean_text(input_text):
    replace = r'[/(){}\[\]|@âÂ,;\?\'\"\*…؟–’،!&\+-:؛-]'
    out_text = re.sub(replace, " ", input_text)
    words = nltk.word_tokenize(out_text)
    words = [word for word in words if word.isalpha()]
    out_text = ' '.join(words)
    return out_text

# Usuwanie wokalizacji w tekście arabskim
def remove_vowelization(input_text):
    vowelization = re.compile(""" [ًٌٍَُِّْـ]""", re.VERBOSE)
    out_text = re.sub(vowelization, '', input_text)
    return out_text

# Usuwanie stopwords:
# Jak przyimki i myślniki. Na przykład [**and, in, or ...etc**].
def delete_stopwords(input_text):
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokenizer = nltk.tokenize.WhitespaceTokenizer()
    tokens = tokenizer.tokenize(input_text)
    wnl = nltk.WordNetLemmatizer()
    lemmatizedTokens = [wnl.lemmatize(t) for t in tokens]
    out_text = [w for w in lemmatizedTokens if w not in stop_words]
    out_text = ' '.join(out_text)
    return out_text

# Tylko dla tekstu arabskiego, ponieważ da nam lepsze wyniki podczas trenowania modeli
def stem_text(input_text):
    st = ISRIStemmer()
    tokenizer = nltk.tokenize.WhitespaceTokenizer()
    tokens = tokenizer.tokenize(input_text)
    out_text = [st.stem(w) for w in tokens]
    out_text = ' '.join(out_text)
    return out_text

# Przygotowanie tekstu:
# Zastosowanie wszystkich wcześniejszych funkcji do sterylizacji wejściowego tekstu.
# Konwersja liter na małe litery, aby wszystkie słowa w tekście miały tę samą wrażliwość na wielkość liter.
def text_prepare(input_text):
    out_text = delete_links(input_text)
    out_text = delete_repeated_characters(out_text)
    out_text = clean_text(out_text)
    out_text = delete_stopwords(out_text)
    out_text = out_text.lower()
    return out_text

# Zastosowanie funkcji przygotowania tekstu do angielskiego i arabskiego zestawu danych
en_data['Processed Text'] = en_data['Text'].apply(text_prepare, args=())

# Koder etykiet
# Konwersja etykiet na wartości numeryczne, aby modele uczące się maszynowo mogły się nimi posługiwać
en_label_encoder = LabelEncoder()
en_data['Category Encoded'] = en_label_encoder.fit_transform(en_data['Category'])


# Podział danych na treningowe i testowe
# 80% danych używanych do trenowania modeli
# 20% danych używanych do testowania i walidacji
en_X_train, en_X_test, en_y_train, en_y_test = train_test_split(en_data['Processed Text'], en_data['Category Encoded'], test_size=0.2, random_state=0)

# Wektoryzator TF-IDF:
# Drugie podejście rozszerza ramy worka słów, uwzględniając całkowite częstotliwości słów w korpusach.
# Pomaga to karać zbyt częste słowa i zapewnia lepszą przestrzeń cech.
def tfidf_features(X_train, X_test, ngram_range):
    tfidf_vectorizer = TfidfVectorizer(min_df=2, max_df=0.5, ngram_range=(1, ngram_range))
    X_train = tfidf_vectorizer.fit_transform(X_train)
    X_test = tfidf_vectorizer.transform(X_test)
    return X_train, X_test

# Podsumowanie i przewidywanie dla wejściowego tekstu:
def summarize_category(input_text, statements, model_name):
    statements = int(statements)
    summary_text = nltk_summarizer(input_text, statements)
    input_text_arr = [text_prepare(input_text)]
    features_train, features_test = tfidf_features(en_X_train, input_text_arr, 2)
    text_prediction = model_name.predict(features_test.toarray())
    text_category = categories[text_prediction[0]]
    return summary_text, text_category

# Funkcja pobierania danych z URL:
def fetch_data(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e} \n")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return fetched_text