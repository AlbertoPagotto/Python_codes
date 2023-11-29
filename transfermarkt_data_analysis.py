import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


current_directory=os.path.dirname(os.path.realpath(__file__))
correlation_array=[]
year_min=2005
year_max=2022
year_array=np.arange(year_min,year_max+1)
season_array=[f"{year}-\n{year+1}" for year in year_array]
for index,year in enumerate(year_array):
    name_csv=f'Fees_{year}_alle__.csv'
    df=pd.read_csv(f'{current_directory}\data\{name_csv}')
    # print(df.describe())
    plt.figure(index)
    sns.pairplot(df)
    plt.savefig(f'{current_directory}\data\Pairplots\Pairplot_{year}.png')
    correlation=df['Fee'].corr(df['Value'])
    correlation_array.append(correlation)

plt.figure(len(year_array)+1)
plt.plot(season_array,correlation_array)
plt.title('Correlation between the transfer fee and the market value')
plt.xlabel('Season')
plt.xticks(season_array)
plt.ylabel('Correlation')
plt.savefig(f'{current_directory}\data\Corr_fee_value.png')
#plt.show()

