import glob
import os
import pandas as pd
import re
from pythainlp import word_tokenize


def contact_list(list):
    string = ''.join(list)
    # re.sub('[^A-Za-z0-9]+', '', string)
    string = " ".join(string.split())
    return string


def cleaning(path_, file_name_, format_):
    if format_ == ".json":
        input_df = pd.read_json(path_ + '/' + file_name_ + format_, encoding='utf-8')
    else:
        input_df = pd.read_csv(path_ + '/' + file_name_ + format_, encoding='utf-8')

    output_df = pd.DataFrame()
    input_length = len(input_df)

    for index, row in input_df.iterrows():
        print(index+1, " of ", input_length, row['title'])

        if len(row['summary']) == 0 or len(row['body']) == 0 or len(row['tags']) == 0:
            continue

        if len(row['summary']) >= len(row['body']):
            continue

        if len(word_tokenize(contact_list(row['body']), engine='newmm', keep_whitespace=False)) <= 225:
            continue

        if len(word_tokenize(contact_list(row['summary']), engine='newmm', keep_whitespace=False)) < 8:
            continue

        if "ภาพจาก" in row['summary'][0]:
            continue

        if "ดวง" in contact_list(row['tags']) \
                or "นิยาย" in contact_list(row['tags']) \
                or "อินสตราแกรมดารา" in contact_list(row['tags']) \
                or "คลิปสุดฮา" in contact_list(row['tags']) \
                or "สรุปข่าว" in contact_list(row['tags']):
            continue

        for x in range(0, len(row['summary'])):
            if row['summary'][x] in row['body']:
                row['body'].remove(row['summary'][x])
            row['summary'][x] = row['summary'][x].replace(".....", "")
            row['summary'][x] = row['summary'][x].replace("....", "")
            row['summary'][x] = row['summary'][x].replace("...", "")
            row['summary'][x] = row['summary'][x].replace("..", "")
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '•'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '‘'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '’'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '“'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '”'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '!'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '\"'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '\''), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '"'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '\"'), None))
            row['summary'][x] = row['summary'][x].translate(dict.fromkeys(map(ord, '!'), None))

        for x in range(0, len(row['body'])):

            row['body'][x] = row['body'][x].replace("อ่านข่าวที่เกี่ยวข้อง", "")
            row['body'][x] = row['body'][x].replace(".....", "")
            row['body'][x] = row['body'][x].replace("....", "")
            row['body'][x] = row['body'][x].replace("...", "")
            row['body'][x] = row['body'][x].replace("..", "")
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '‘'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '’'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '“'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '”'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '!'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '\"'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '\''), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '"'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '\"'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '!'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '•'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '\u200b'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '"'), None))
            row['body'][x] = row['body'][x].translate(dict.fromkeys(map(ord, '\"'), None))

        for x in range(0, len(row['title'])):
            row['title'][x] = row['title'][x].replace(".....", "")
            row['title'][x] = row['title'][x].replace("....", "")
            row['title'][x] = row['title'][x].replace("...", "")
            row['title'][x] = row['title'][x].replace("..", "")
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '•'), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '‘'), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '’'), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '“'), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '”'), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '!'), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '\"'), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '\''), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '"'), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '\"'), None))
            row['title'][x] = row['title'][x].translate(dict.fromkeys(map(ord, '!'), None))

        for x in range(0, len(row['tags'])):
            row['tags'][x] = row['tags'][x].replace(".....", "")
            row['tags'][x] = row['tags'][x].replace("....", "")
            row['tags'][x] = row['tags'][x].replace("...", "")
            row['tags'][x] = row['tags'][x].replace("..", "")
            row['tags'][x] = row['tags'][x].translate(dict.fromkeys(map(ord, '•'), None))
            row['tags'][x] = row['tags'][x].translate(dict.fromkeys(map(ord, '‘'), None))
            row['tags'][x] = row['tags'][x].translate(dict.fromkeys(map(ord, '’'), None))
            row['tags'][x] = row['tags'][x].translate(dict.fromkeys(map(ord, '“'), None))
            row['tags'][x] = row['tags'][x].translate(dict.fromkeys(map(ord, '”'), None))
            row['tags'][x] = row['tags'][x].translate(dict.fromkeys(map(ord, '!'), None))
            row['tags'][x] = row['tags'][x].translate(dict.fromkeys(map(ord, '\"'), None))
            row['tags'][x] = row['tags'][x].translate(dict.fromkeys(map(ord, '\''), None))
            row['tags'][x] = row['tags'][x].translate(dict.fromkeys(map(ord, '"'), None))
            row['tags'][x] = row['tags'][x].translate(dict.fromkeys(map(ord, '\"'), None))
            row['tags'][x] = row['tags'][x].translate(dict.fromkeys(map(ord, '!'), None))

        output_df.loc[index, 'title'] = contact_list(row['title'])
        output_df.loc[index, 'body'] = contact_list(row['body'])
        output_df.loc[index, 'summary'] = contact_list(row['summary'])
        output_df.loc[index, 'tags'] = str(row['tags'])

        input_df.drop(index, inplace=True)

    subdirectory = "cleaned_csv"
    try:
        os.mkdir(subdirectory)
    except FileExistsError:
        pass
    output_df.to_csv(os.path.join(subdirectory, "cleaned_" + file_name_ + ".csv"), index=False, encoding='utf-8-sig',
              columns=["title", "body", "summary", "tags"])


# START HERE
path = "E:\\Khun Projects\\Thairath_Crawler\\test_dataset"
os.chdir(path)

all_filenames = [i for i in glob.glob('*.{}'.format("json"))]
sorted(all_filenames)
k = 1
for file_name in all_filenames:
    print("Cleaning ", k, " of ", len(all_filenames))
    file_name = file_name.replace(".json", "")
    print("\n", str(file_name))
    cleaning(path, file_name, ".json")
    k = k + 1
