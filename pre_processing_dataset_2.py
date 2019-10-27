import csv
import glob
import os
import pandas as pd
import re

def cleaning(path_, file_name_, format_):

    new_df = pd.DataFrame(columns=["body", "summary", "abstractedness"])

    if format_ == ".json":
        df = pd.read_json(path_ + '/' + file_name_ + format_, encoding='utf-8')
    else:
        df = pd.read_csv(path_ + '/' + file_name_ + format_, encoding='utf-8')

    for index, row in df.iterrows():
        percent = (index * 100) / len(df)
        print(index, " of ", len(df.index), " || ", percent)

        row['body'] = row['body'].replace("..", "")
        row['body'] = row['body'].replace("...", "")
        row['body'] = row['body'].replace("....", "")
        row['body'] = row['body'].replace(".....", "")
        row['body'] = row['body'].replace("‘", "")
        row['body'] = row['body'].replace("’", "")
        row['body'] = row['body'].replace("“", "")
        row['body'] = row['body'].replace("”", "")
        row['body'] = row['body'].replace("!", "")
        row['body'] = row['body'].replace("\"", "")
        row['body'] = row['body'].replace("\'", "")

        row['summary'] = row['summary'].replace("..", "")
        row['summary'] = row['summary'].replace("...", "")
        row['summary'] = row['summary'].replace("....", "")
        row['summary'] = row['summary'].replace(".....", "")
        row['summary'] = row['summary'].replace("‘", "")
        row['summary'] = row['summary'].replace("’", "")
        row['summary'] = row['summary'].replace("“", "")
        row['summary'] = row['summary'].replace("”", "")
        row['summary'] = row['summary'].replace("!", "")
        row['summary'] = row['summary'].replace("\"", "")
        row['summary'] = row['summary'].replace("\'", "")

        new_df.loc[index, 'body'] = row['body']
        new_df.loc[index, 'summary'] = row['summary']
        new_df.loc[index, 'abstractedness'] = row['abstractedness']

    subdirectory = "cleaned_csv"
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass

    new_df.to_csv(os.path.join(subdirectory, "cleaned_" + file_name_ + ".csv"), index=False,
              encoding='utf-8-sig',
              columns=["body", "summary", "abstractedness"])


# START HERE
path = "E:\\Khun Projects\\Thairath_Crawler\\detail"
os.chdir(path)
cleaning(path, "thairath-201k_statistic", ".csv")
