import pandas as pd
import os

path = "E:\\Khun Projects\\Thairath_Crawler\\detail\\cleaned_thairath_detail.csv"
thairath_df = pd.read_csv(path, encoding='utf-8')
df_size = len(thairath_df)

for index, row in thairath_df.iterrows():
    if row['abstractedness'] >= 50:
        thairath_df.drop(index, inplace=True)
        continue

    percent = (index * 100) / df_size
    print("\n", index, " of ", df_size, " || ", percent, "%")

subdirectory = "detail"
file_name_ = "thairath_detail_remove_abstract"
try:
    os.mkdir(subdirectory)
except Exception:
    pass
thairath_df.to_csv(os.path.join(subdirectory, "cleaned_" + file_name_ + ".csv"), index=False, encoding='utf-8-sig',
                   columns=["body", "summary"])
