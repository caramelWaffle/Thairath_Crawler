import pandas as pd
import tltk
import os

path = "E:\\Khun Projects\\Thairath_Crawler\\test_dataset\\test_data200.csv"
thairath_df = pd.read_csv(path, encoding='utf-8')
df_size = len(thairath_df)

for index, row in thairath_df.iterrows():
    # bi_gram = tltk.nlp.word_segment_nbest(row['body'], 2)
    bi_gram = tltk.nlp.word_segment(row['body'], 'ngram')
    thairath_df.loc[index, '2-gram'] = bi_gram
    percent = (index * 100) / df_size
    print("\n", index, " of ", df_size, " || ", percent, "%")
    print("\n", bi_gram)


subdirectory = "detail"
file_name_ = "thairath_detail_2_gram"

try:
    os.mkdir(subdirectory)
except Exception:
    pass

thairath_df.to_csv(os.path.join(subdirectory, "cleaned_" + file_name_ + ".csv"),
                   index=False, encoding='utf-8-sig',
                   columns=["body", "2-gram"])
