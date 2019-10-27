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


def cleaning(path_, file_name_, format_):
    if format_ == ".json":
        df = pd.read_json(path_ + '/' + file_name_ + format_, encoding='utf-8')
    else:
        df = pd.read_csv(path_ + '/' + file_name_ + format_, encoding='utf-8')

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

        if len(word_tokenize(contact_list(row['body']), engine='newmm', keep_whitespace=False)) <= 230:
            df.drop(index, inplace=True)
            continue

        if len(word_tokenize(contact_list(row['summary']), engine='newmm', keep_whitespace=False)) < 8:
            df.drop(index, inplace=True)
            continue

        if "ภาพจาก" in row['summary'][0]:
            df.drop(index, inplace=True)
            continue

        if "ดวง" in contact_list(row['tags']) \
                or "นิยาย" in contact_list(row['tags']) \
                or "อินสตราแกรมดารา" in contact_list(row['tags']) \
                or "คลิปสุดฮา" in contact_list(row['tags']) \
                or "สรุปข่าว" in contact_list(row['tags']):
            df.drop(index, inplace=True)
            continue

        for x in range(0, len(row['summary'])):
            row['body'].remove(row['summary'][x])
            row['summary'][x] = row['summary'][x].replace("‘", "")
            row['summary'][x] = row['summary'][x].replace("’", "")
            row['summary'][x] = row['summary'][x].replace("“", "")
            row['summary'][x] = row['summary'][x].replace("”", "")
            row['summary'][x] = row['summary'][x].replace("!", "")
            row['summary'][x] = row['summary'][x].replace("\"", "")
            row['summary'][x] = row['summary'][x].replace("\'", "")
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '..'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '...'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '....'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '....'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '"'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '\"'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '!'), None))

        for x in range(0, len(row['body'])):
            row['body'][x] = row['body'][x].replace("อ่านข่าวที่เกี่ยวข้อง", "")
            row['body'][x] = row['body'][x].replace("‘", "")
            row['body'][x] = row['body'][x].replace("’", "")
            row['body'][x] = row['body'][x].replace("“", "")
            row['body'][x] = row['body'][x].replace("”", "")
            row['body'][x] = row['body'][x].replace("!", "")
            row['body'][x] = row['body'][x].replace("\"", "")
            row['body'][x] = row['body'][x].replace("\'", "")
            row['body'][x] = row['body'][x].replace("•", "")
            row['body'][x] = row['body'][x].replace("\u200b", "")
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '..'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '...'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '....'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '"'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '\"'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '•'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, 'u200b'), None))



        for x in range(0, len(row['title'])):
            row['title'][x] = row['title'][x].replace("ชมคลิป", "")
            row['title'][x] = row['title'][x].replace("‘", "")
            row['title'][x] = row['title'][x].replace("’", "")
            row['title'][x] = row['title'][x].replace("“", "")
            row['title'][x] = row['title'][x].replace("”", "")
            row['title'][x] = row['title'][x].replace("\'", "")
            row['title'][x] = row['title'][x].replace("\"", "")
            row['title'][x] = row['title'][x].replace("!", "")
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '..'), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '...'), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '....'), None))

        title_list.append(contact_list(row['title']))
        body_list.append(contact_list(row['body']))
        summary_list.append(contact_list(row['summary']))

    del df['summary']
    del df['body']
    # del df['title']

    df['summary'] = summary_list
    df['body'] = body_list
    # df['title'] = title_list

    subdirectory = "cleaned_csv"
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass
    df.to_csv(os.path.join(subdirectory, "cleaned_" + file_name_ + ".csv"), index=False, encoding='utf-8-sig',
              columns=["body", "summary"])


# START HERE
path = "E:\\Khun Projects\\Thairath_Crawler\\detail"
os.chdir(path)
# cleaning(path, "cleaned_thairath_detail_test_200", ".csv")

all_filenames = [i for i in glob.glob('*.{}'.format("json"))]
sorted(all_filenames)
k = 1
for file_name in all_filenames:
    print("Cleaning ", k, " of ", len(all_filenames))
    file_name = file_name.replace(".json", "")
    print("\n", str(file_name))
    cleaning(path, file_name)
    k = k + 1
