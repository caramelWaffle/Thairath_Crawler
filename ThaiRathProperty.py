import pythainlp
import pandas as pd
import tltk
from thai_segmenter import line_sentence_segmenter
from thai_segmenter import sentence_segment
from pythainlp.util import *


path = "/Users/macintoshhd/Thairath_Crawler/dataset/test_data200.csv"
thairath_df = pd.read_csv(path, encoding='utf-8')

all_labels = list()
article_token = list()
summary_token = list()
ab_score = 0
abstract_percent = 0

for index, row in thairath_df.iterrows():

    article_token.clear()
    summary_token.clear()

    for token in pythainlp.word_tokenize(row['body'], engine='newmm'):
        all_labels.append(token)
        article_token.append(token)

    for token in pythainlp.word_tokenize(row['summary'], engine='newmm'):
        all_labels.append(token)
        summary_token.append(token)

    thairath_df.loc[index, 'article_lenght'] = len(pythainlp.word_tokenize(row['body'], engine='newmm'))
    thairath_df.loc[index, 'summary_lenght'] = len(pythainlp.word_tokenize(row['summary'], engine='newmm'))

    article_set = set(article_token)
    summary_set = set(summary_token)

    ab_score = 0
    abstract_percent = 0

    for summary in summary_set:
        if summary not in article_set:
            ab_score = ab_score + 1

    abstract_percent = (ab_score * 100)/len(article_set)
    thairath_df.loc[index, 'abstractedness'] = abstract_percent

    print("\n =======================================================")
    print("\n", article_token)
    print("\n", summary_token)
    print(abstract_percent)
    # print(tltk.nlp.word_segment_nbest(row['body'], 2))

    # sentences = sentence_segment(row['body'])
    # for sentence in sentences:
    #     print("\n", str(sentence))

article_avg_size = thairath_df['article_lenght'].mean()
summary_avg_size = thairath_df['summary_lenght'].mean()
abstract_avg_size = thairath_df['abstractedness'].mean()

unique_set = set(all_labels)

print("\nDataset size : ", len(thairath_df))
print("Article_avg_size : ", article_avg_size)
print("Summary_avg_size : ", summary_avg_size)
print("Vocabulary : ", len(unique_set))
print("Abstract_avg_size : ", abstract_avg_size)
