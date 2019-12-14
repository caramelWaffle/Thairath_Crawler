import pandas as pd
import os
import numpy as np
from tqdm import tqdm
# File
df = pd.read_csv("E:\\Khun Projects\\Thairath_Crawler\\thairath_spider\\test_dataset_for_counting.csv", encoding='utf-8')

# # Functions
# meta_no_art = df.query('meta_sum.notnull()', engine='python').query('article_sum.isnull()', engine='python')
# art_no_meta = df.query('article_sum.notnull()', engine='python').query('meta_sum.isnull()', engine='python')
# no_both_art_meta = df.query('article_sum.isnull()', engine='python').query('meta_sum.isnull()', engine='python')
# have_both = df.query('article_sum.notnull()', engine='python').query('meta_sum.notnull()', engine='python')
#
# # Print
# print("Meta_no_art : ", len(meta_no_art))
# print(meta_no_art.head(20).url)
# print("Art_no_meta : ", len(art_no_meta))
# print(art_no_meta.head(20).url)
# print("No_both_art_meta : ", len(no_both_art_meta))
# print("Have both : ", len(have_both))

output_name = "assign_sum.csv"
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    output_df = pd.DataFrame()
    if pd.isnull(row['article_sum']) and pd.isnull(row['meta_sum']):
        continue

    output_df.loc[index, 'title'] = row['title']
    output_df.loc[index, 'body'] = row['body']
    output_df.loc[index, 'type'] = row['type']
    output_df.loc[index, 'tags'] = row['tags']
    output_df.loc[index, 'url'] = row['url']
    output_df.loc[index, 'date'] = row['date']
    output_df.loc[index, 'summary'] = row['meta_sum'] if pd.isnull(row['article_sum']) else row['article_sum']

    if not os.path.isfile(output_name):
        output_df.to_csv(output_name, index=False, encoding='utf-8-sig',
                         header=["title", "body", "summary", "type", "tags", "url", "date"])
    else:  # else it exists so append without writing the header
        output_df.to_csv(output_name, index=False, encoding='utf-8-sig', mode='a', header=False)
