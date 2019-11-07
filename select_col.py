import os
import pandas as pd

df = pd.read_csv("test_data200.csv", encoding='utf-8', usecols=['body', 'summary'])


df.to_csv(os.path.join("bodyandsum.csv"), index=False, encoding='utf-8',
                 columns=['body', 'summary'])
