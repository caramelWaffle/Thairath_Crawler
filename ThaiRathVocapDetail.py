import pythainlp
import pandas as pd
import pickle
import os


def contact_list(list):
    string = ''.join(list)
    string = " ".join(string.split())
    return string


path = 'E:\\Khun Projects\\Thairath_Crawler\\detail\\'
file_name = 'thairath-228k'
thairath_df = pd.read_csv(path+file_name+'.csv', encoding='utf-8')
pickle_name = "vocab.pkl"
pickle_unique_name = "vocab_unique.pkl"
local_file = "vocab_item.txt"
df_size = len(thairath_df)
os.chdir(path)

for index, row in thairath_df.iterrows():
    title_token = pythainlp.word_tokenize(row['title'], engine='newmm', keep_whitespace=False)
    article_token = pythainlp.word_tokenize(row['body'], engine='newmm', keep_whitespace=False)
    summary_token = pythainlp.word_tokenize(row['summary'], engine='newmm', keep_whitespace=False)
    tag_token = pythainlp.word_tokenize(contact_list(row['tags']), engine='newmm', keep_whitespace=False)

    thairath_df.loc[index, 'title_length'] = len(title_token)
    all_token = set(title_token + article_token + summary_token)

    with open(pickle_name, 'ab') as file:
        pickle.dump(list(all_token), file)
    all_token.clear()

    percent = (index * 100) / df_size
    print("Tokenization - [step 1 of 2 ] ", index + 1, " of ", df_size, " || ", percent, "%")

vocab_set = set()
with open(pickle_name, 'rb') as file:
    for i in range(df_size):
        vocab_set.update(pickle.load(file))
        percent = ((i+1) * 100) / df_size
        print("Uniquify Token - [step 2 of 2 ] ", i + 1, " of ", df_size, " || ", percent, "%")

with open(pickle_unique_name, 'wb') as file:
    print("Saving unique vocab...")
    pickle.dump(list(vocab_set), file)
    file.close()

print("Writing result...")
file = open(local_file, "w+", encoding="utf-8")
file.write(str(vocab_set))
file.close()

print("\nVocab size : ", len(vocab_set))
print("File detailed at ", path, local_file)