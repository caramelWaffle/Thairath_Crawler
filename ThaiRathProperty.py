import pythainlp
import pandas as pd
import os


def get_abstractedness_score(article_set, summary_set):
    ab_score = 0
    for summary in summary_set:
        if summary not in article_set:
            ab_score = ab_score + 1
    return (ab_score * 100) / len(summary_set)


def generate_ngrams(tokens, n):
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return ["".join(ngram) for ngram in ngrams]


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%d%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


path = 'E:\\Khun Projects\\Thairath_Crawler\\test_dataset\\cleaned_csv\\'
file_name = 'thairath-250k.csv'
thairath_df = pd.read_csv(path+file_name, encoding='utf-8')

df_size = len(thairath_df)
for index, row in thairath_df.iterrows():

    if len(pythainlp.word_tokenize(row['summary'], engine='newmm', keep_whitespace=False)) < 5:
        continue

    article_token = pythainlp.word_tokenize(row['body'], engine='newmm', keep_whitespace=False)
    summary_token = pythainlp.word_tokenize(row['summary'], engine='newmm', keep_whitespace=False)
    title_token = pythainlp.word_tokenize(row['title'], engine='newmm', keep_whitespace=False)

    thairath_df.loc[index, 'article_length'] = len(article_token)
    thairath_df.loc[index, 'summary_length'] = len(summary_token)
    thairath_df.loc[index, 'title_length'] = len(title_token)

    thairath_df.loc[index, 'abstractedness_n1'] = get_abstractedness_score(set(article_token), set(summary_token))

    if thairath_df.loc[index, 'abstractedness_n1'] > 65:
        thairath_df.drop(index, inplace=True)
        continue

    # thairath_df.loc[index, 'abstractedness_n2'] = get_abstractedness_score(set(generate_ngrams(article_token, 2)),
    #                                                                        set(generate_ngrams(summary_token, 2)))
    # thairath_df.loc[index, 'abstractedness_n3'] = get_abstractedness_score(set(generate_ngrams(article_token, 3)),
    #                                                                        set(generate_ngrams(summary_token, 3)))
    # thairath_df.loc[index, 'abstractedness_n4'] = get_abstractedness_score(set(generate_ngrams(article_token, 4)),
    #                                                                        set(generate_ngrams(summary_token, 4)))
    # thairath_df.loc[index, 'abstractedness_n5'] = get_abstractedness_score(set(generate_ngrams(article_token, 5)),
    #                                                                        set(generate_ngrams(summary_token, 5)))
    percent = (index * 100) / df_size
    print(index+1, " of ", df_size, " || ", percent)

article_avg_size = thairath_df['article_length'].mean()
summary_avg_size = thairath_df['summary_length'].mean()
title_avg_size = thairath_df['title_length'].mean()

abstract_avg_size = thairath_df['abstractedness_n1'].mean()
# abstract_avg_size_2 = thairath_df['abstractedness_n2'].mean()
# abstract_avg_size_3 = thairath_df['abstractedness_n3'].mean()
# abstract_avg_size_4 = thairath_df['abstractedness_n4'].mean()
# abstract_avg_size_5 = thairath_df['abstractedness_n5'].mean()

print("\nDataset size : ", len(thairath_df))
print("Title_avg_size : ", title_avg_size)
print("Article_avg_size : ", article_avg_size)
print("Summary_avg_size : ", summary_avg_size)
print("Abstract_avg_size : ", abstract_avg_size)
# print("Abstract_2_avg_size : ", abstract_avg_size_2)
# print("Abstract_3_avg_size : ", abstract_avg_size_3)
# print("Abstract_4_avg_size : ", abstract_avg_size_4)
# print("Abstract_5_avg_size : ", abstract_avg_size_5)


subdirectory = "detail"

file = open("thairath-"+human_format(len(thairath_df))+".txt", "w+")
file.write("Dataset size : " + str(len(thairath_df)))
file.write("\nTitle_avg_size : " + str(title_avg_size))
file.write("\nArticle_avg_size : " + str(article_avg_size))
file.write("\nSummary_avg_size : " + str(summary_avg_size))
# file.write("\nAbstract_2_avg_size : " + str(abstract_avg_size_2))
# file.write("\nAbstract_3_avg_size : " + str(abstract_avg_size_3))
# file.write("\nAbstract_4_avg_size : " + str(abstract_avg_size_4))
# file.write("\nAbstract_5_avg_size : " + str(abstract_avg_size_5))
file.close()

try:
    os.mkdir(subdirectory)
except FileExistsError:
    pass
thairath_df.to_csv(os.path.join(subdirectory, "Published_" + file_name + ".csv"), index=False, encoding='utf-8-sig',
                   columns=["title", "body", "summary", "tags"])
