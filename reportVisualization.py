import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Data/DataItviec.csv')
jobTag_count = df['jobTag'].value_counts()
# sns.barplot( jobTag_count[:20].values,jobTag_count[:20].index )
# plt.ylabel('Job name')
# plt.xlabel('Number job')
jobTag_count[:20].plot(kind='barh', rot=0)
plt.ylabel('Job name')
plt.xlabel('Number job')