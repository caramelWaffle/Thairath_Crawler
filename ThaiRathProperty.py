import pythainlp
import pandas as pd
import os

path = "E:\\Khun Projects\\Thairath_Crawler\\test_10.csv"
thairath_df = pd.read_csv(path, encoding='utf-8')


def get_abstractedness_score(article_set, summary_set):
    ab_score = 0
    for summary in summary_set:
        if summary not in article_set:
            ab_score = ab_score + 1
    return (ab_score * 100) / len(summary_set_n1)


def generate_ngrams(tokens, n):
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return ["".join(ngram) for ngram in ngrams]


for index, row in thairath_df.iterrows():

    article_token = pythainlp.word_tokenize(row['body'], engine='newmm', keep_whitespace=False)
    summary_token = pythainlp.word_tokenize(row['summary'], engine='newmm', keep_whitespace=False)

    thairath_df.loc[index, 'article_length'] = len(article_token)
    thairath_df.loc[index, 'summary_length'] = len(summary_token)

    article_set_n1 = set(article_token)
    summary_set_n1 = set(summary_token)

    article_set_n2 = set(generate_ngrams(article_token, 2))
    summary_set_n2 = set(generate_ngrams(summary_token, 2))

    thairath_df.loc[index, 'abstractedness_n1'] = get_abstractedness_score(article_set_n1, summary_set_n1)
    thairath_df.loc[index, 'abstractedness_n2'] = get_abstractedness_score(article_set_n2, summary_set_n2)

    percent = (index * 100) / len(thairath_df)
    print("\n", index, " of ", len(thairath_df), " || ", percent, "%")

article_avg_size = thairath_df['article_length'].mean()
summary_avg_size = thairath_df['summary_length'].mean()
abstract_avg_size = thairath_df['abstractedness'].mean()
abstract_avg_size_2 = thairath_df['abstractedness_n2'].mean()

print("Dataset size : ", len(thairath_df))
print("Article_avg_size : ", article_avg_size)
print("Summary_avg_size : ", summary_avg_size)
print("Abstract_avg_size : ", abstract_avg_size)
print("Abstract_2_avg_size : ", abstract_avg_size_2)

subdirectory = "detail"
file_name_ = "thairath_201k-edit-statistic"
try:
    os.mkdir(subdirectory)
except FileExistsError:
    pass
thairath_df.to_csv(os.path.join(subdirectory, "cleaned_" + file_name_ + ".csv"), index=False, encoding='utf-8-sig',
                   columns=["body", "summary", "article_length", "summary_length", "abstractedness_n1",
                            "abstractedness_n2"])
