import glob
import os
import pandas as pd
import re
from pythainlp import word_tokenize


def contact_list(list):
    string = ''.join(list)
    re.sub('[^A-Za-z0-9]+', '', string)
    string = " ".join(string.split())
    return string


def cleaning(path_, file_name_):
    df = pd.read_json(path_ + '/' + file_name_ + '.json', encoding='utf8')
    # df = df[['title', 'body', 'summary', 'tags']]
    summary_list = []
    body_list = []
    title_list = []
    print("Raw dataset")

    for index, row in df.iterrows():
        print(index, " of ", max(df.index), row['title'])

        if len(row['summary']) == 0 or len(row['body']) == 0 or len(row['tags']) == 0:
            df.drop(index, inplace=True)
            continue

        if len(row['summary']) >= len(row['body']):
            df.drop(index, inplace=True)
            continue

        if len(word_tokenize(contact_list(row['body']), engine='newmm', keep_whitespace=False)) <= 150:
            df.drop(index, inplace=True)
            continue

        if "ภาพจาก" in row['summary'][0]:
            df.drop(index, inplace=True)
            continue

        if "ดวง" in contact_list(row['tags']) \
                or "นิยาย" in contact_list(row['tags']) \
                or "อินสตราแกรมดารา" in contact_list(row['tags']) \
                or "สรุปข่าว" in contact_list(row['tags']):
            df.drop(index, inplace=True)
            continue

        row['body'].remove(row['summary'][0])
        row['summary'][0] = row['summary'][0].replace("...", "")

        for x in range(0, len(row['body'])):
            row['body'][x] = row['body'][x].replace("อ่านข่าวที่เกี่ยวข้อง", "")

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

    subdirectory = "cleaned_csv"
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass

    # with open(os.path.join(subdirectory, ip.strip() + ".txt"), "a") as ip_file:
    # with open(os.path.join(subdirectory,"cleaned_" + file_name + ".json"), 'w', encoding='utf-8') as file:
    #     df.to_json(file, force_ascii=False)

    # df.to_json(os.path.join(subdirectory, "cleaned_" + file_name + ".json"), orient='records', lines=True, force_ascii=False)
    df.to_csv(os.path.join(subdirectory, "cleaned_" + file_name_ + ".csv"), index=False, encoding='utf-8-sig',
              columns=["title", "body", "summary", "tags"])


# START HERE
path = "E:\Khun Projects\Thairath_Crawler\\test_dataset"
os.chdir(path)
all_filenames = [i for i in glob.glob('*.{}'.format("json"))]
sorted(all_filenames)
k = 1
for file_name in all_filenames:
    print("Cleaning ", k, " of ", len(all_filenames))
    file_name = file_name.replace(".json", "")
    print("\n", str(file_name))
    cleaning(path, file_name)
    k = k + 1
