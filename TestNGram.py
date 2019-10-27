import pythainlp
import pandas as pd
import nltk
from sklearn.feature_extraction.text import CountVectorizer


def generate_ngrams(tokens, n):
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return ["".join(ngram) for ngram in ngrams]


df = pd.read_csv("/Users/macintoshhd/Thairath_Crawler/test_10.csv", encoding="utf-8")
token_body = []
token_summary = []

for index, row in df.iterrows():
    token_body = pythainlp.word_tokenize(row['body'], keep_whitespace=False)
    token_summary = pythainlp.word_tokenize(row['summary'], keep_whitespace=False)

    vectorizer = CountVectorizer(ngram_range=(2, 2), encoding="utf-8")
    vectorizer.fit(token_body)
    print("token = ", token_body)
    print("vectorizer = ", generate_ngrams(token_body, 2))

    # for string in row['body'].split(' '):
    #     print(string, "|")

