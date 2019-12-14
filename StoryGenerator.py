import pandas as pd
import os
import math

df = pd.read_csv('detail/thairath-228k_body_Sum.csv', encoding='utf-8')
subdirectory = "story"
num = 0
mean_ab1 = 0
mean_ab2 = 0
mean_ab3 = 0
mean_ab4 = 0
mean_ab5 = 0
df_size = len(df)

try:
    os.mkdir(subdirectory)
except FileExistsError:
    pass

for index, row in df.iterrows():

    try:
        if math.isnan(float(row['abstractedness_n1'])):
            print("Nan at index ", index)
            df.drop(index, inplace=True)
            continue
    except ValueError:
        df.drop(index, inplace=True)
        continue

    if float(row['abstractedness_n4']) > 50:
        df.drop(index, inplace=True)
        continue

    num = num + 1

    mean_ab1 = mean_ab1 + float(row['abstractedness_n1'])
    mean_ab2 = mean_ab2 + float(row['abstractedness_n2'])
    mean_ab3 = mean_ab3 + float(row['abstractedness_n3'])
    mean_ab4 = mean_ab4 + float(row['abstractedness_n4'])
    mean_ab5 = mean_ab5 + float(row['abstractedness_n5'])

    file_name = os.path.join(subdirectory,f"thairath_story_{num}.story")
    file = open(file_name, "w+", encoding="utf-8")
    file.write(row['body'] + '\n\n')
    file.write('@highlight\n\n')
    file.write(row['summary'])
    file.close()

    abstract_avg_size = mean_ab1 / num
    abstract_avg_size_2 = mean_ab2 / num
    abstract_avg_size_3 = mean_ab3 / num
    abstract_avg_size_4 = mean_ab4 / num
    abstract_avg_size_5 = mean_ab5 / num


    percent = (index * 100) / df_size
    print(f'\nTotal file : {num}')
    print(f"{index + 1} of {df_size} || {percent}%")
    print("Abstract_avg_size : ", abstract_avg_size)
    print("Abstract_2_avg_size : ", abstract_avg_size_2)
    print("Abstract_3_avg_size : ", abstract_avg_size_3)
    print("Abstract_4_avg_size : ", abstract_avg_size_4)
    print("Abstract_5_avg_size : ", abstract_avg_size_5)

df.to_csv("filtered_thairath-228k_body_Sum.csv", index=False, encoding='utf-8-sig', columns=["body", "summary"])