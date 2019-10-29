import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
df = pd.read_csv("E:\\Khun Projects\\Thairath_Crawler\\abstractedness_compared.csv")
new_df = df.iloc[:, 1:]
new_df = new_df.transpose()
new_df.columns = df['Dataset']
new_df.plot()
# test_df=pd.DataFrame({'x': range(1,11), 'y1': np.random.randn(10), 'y2': np.random.randn(10)+range(1,11), 'y3': np.random.randn(10)+range(11,21) })
# plt.plot(new_df.columns,new_df.columns , data=df, linestyle='dashed')
plt.show()
