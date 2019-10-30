import pythainlp
import pandas as pd

def contact_list(list):
    string = ''.join(list)
    string = " ".join(string.split())
    return string


path = '/Users/macintoshhd/Thairath_Crawler/test_dataset/'
file_name = 'test_data200'
thairath_df = pd.read_csv(path+file_name+'.csv', encoding='utf-8')

df_size = len(thairath_df)

for index, row in thairath_df.iterrows():
    title_token = pythainlp.word_tokenize(row['title'], engine='newmm', keep_whitespace=False)
    article_token = pythainlp.word_tokenize(row['body'], engine='newmm', keep_whitespace=False)
    summary_token = pythainlp.word_tokenize(row['summary'], engine='newmm', keep_whitespace=False)
    tag_token = pythainlp.word_tokenize(contact_list(row['tags']), engine='newmm', keep_whitespace=False)

    thairath_df.loc[index, 'title_length'] = len(title_token)
    percent = (index * 100) / df_size
    print(index + 1, " of ", df_size, " || ", percent, "%")

summary_avg_size = thairath_df['title_length'].mean()

print("\nAvg of title size : ", summary_avg_size)







