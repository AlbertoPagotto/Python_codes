import pandas as pd
import numpy
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('Fees_2022_all_all.csv')
## Turn the age into an int, and 'm' and 'k' into numbers
df['Age']=[int(age) for age in df['Age'].tolist()]
df['Value']=[float(fee[1:-1])*((10**3)*(fee[-1]=='k')+(10**6)*(fee[-1]=='m')) for fee in df['Value'].tolist()]
df['Fee']=[float(fee[1:-1])*((10**3)*(fee[-1]=='k')+(10**6)*(fee[-1]=='m')) for fee in df['Fee'].tolist()]

print(df.describe())
sns.pairplot(df)
plt.show()