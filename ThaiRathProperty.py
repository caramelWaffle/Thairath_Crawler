import pythainlp
import pandas as pd
import pickle
import os

path = "E:/Khun Projects/Thairath_Crawler/detail/thairath-201k-edit.csv"
thairath_df = pd.read_csv(path, encoding='utf-8')
file = "thairath_vocab.pkl"

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

    with open(file, 'ab') as fp:
        pickle.dump(all_labels, fp)
        fp.close()

    thairath_df.loc[index, 'article_length'] = len(pythainlp.word_tokenize(row['body'], engine='newmm'))
    thairath_df.loc[index, 'summary_length'] = len(pythainlp.word_tokenize(row['summary'], engine='newmm'))

    article_set = set(article_token)
    summary_set = set(summary_token)

    ab_score = 0
    abstract_percent = 0

    for summary in summary_set:
        if summary not in article_set:
            ab_score = ab_score + 1

    abstract_percent = (ab_score * 100) / len(summary_set)
    thairath_df.loc[index, 'abstractedness'] = abstract_percent

    percent = (index * 100)/len(thairath_df)
    print("\n", index, " of ", len(thairath_df), " || ", percent, "%")

    all_labels.clear()

    # sentences = sentence_segment(row['body'])
    # for sentence in sentences:
    # print("\n", str(sentence))

article_avg_size = thairath_df['article_length'].mean()
summary_avg_size = thairath_df['summary_length'].mean()
abstract_avg_size = thairath_df['abstractedness'].mean()

# uncomment
# with open(file, 'rb') as fr:
#     for x in range(len(thairath_df)):
#         all_labels = all_labels + pickle.load(fr)
#     fr.close()
#
# unique_set = set(all_labels)

print("\nDataset size : ", len(thairath_df))
print("Article_avg_size : ", article_avg_size)
print("Summary_avg_size : ", summary_avg_size)
# print("Vocabulary : ", len(unique_set))
print("Abstract_avg_size : ", abstract_avg_size)

subdirectory = "detail"
file_name_ = "thairath_201k-edit-statistic"
try:
    os.mkdir(subdirectory)
except Exception:
    pass
thairath_df.to_csv(os.path.join(subdirectory, "cleaned_" + file_name_ + ".csv"), index=False, encoding='utf-8-sig',
                   columns=["body", "summary", "article_length", "summary_length", "abstractedness"])
