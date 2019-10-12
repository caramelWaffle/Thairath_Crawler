import glob
import os
import pandas as pd
import re
from pythainlp import word_tokenize


def contact_list(list):
    string = ''.join(list)
    re.sub('[^A-Za-z0-9]+', '', string)
    return string


def cleaning(path_, file_name_):
    df = pd.read_json(path_ + file_name_)
    summary_list = []
    body_list = []
    title_list = []
    print("Raw dataset")

    for index, row in df.iterrows():
        print(index, row['summary'], row['body'], row['tags'])

        if len(row['summary']) == 0 or len(row['body']) == 0 or len(row['tags']) == 0:
            df.drop(index, inplace=True)
            continue

        if len(row['summary']) >= len(row['body']):
            df.drop(index, inplace=True)
            continue

        if len(word_tokenize(contact_list(row['body']), engine='newmm')) <= 150:
            df.drop(index, inplace=True)
            continue

        if "ภาพจาก" in row['summary'][0]:
            df.drop(index, inplace=True)
            continue

        row['body'].remove(row['summary'][0])
        row['summary'][0] = row['summary'][0].replace("...", "")

        title_list.append(contact_list(row['title']))
        body_list.append(contact_list(row['body']))
        summary_list.append(contact_list(row['summary']))

    del df['summary']
    del df['body']
    del df['title']

    df['summary'] = summary_list
    df['body'] = body_list
    df['title'] = title_list

    print("\nAfter pre-processing")

    for index, row in df.iterrows():
        print(index, "\n", row['title'], "\n", row['summary'], "\n", row['body'], "\n", row['tags'])

    df.to_csv(file_name+"cleaned_.csv", index=False, encoding='utf-8-sig')


# START HERE


path = "/Users/macintoshhd/Thairath_Crawler/test_dataset/"
os.chdir(path)
all_filenames = [i for i in glob.glob('*.{}'.format("json"))]
k = 1
for file_name in all_filenames:
    print("Cleaning ", k, " of ", len(all_filenames))
    cleaning(path, file_name)
    k = k + 1
