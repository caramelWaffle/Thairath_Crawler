import pandas as pd

df = pd.read_csv("dataset/test_data200.csv", encoding='utf-8', usecols=['body', 'summary'])

with open('output.json', 'w', encoding='utf-8', ensure_ascii=False) as file:
    df.to_json(file, force_ascii=False, indent=4)