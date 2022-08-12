# %% Import library
import pandas  as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib import colors

# %%Import dataset
#feature = [BURSA ,20645384,8/3/2022,Fiat,Linea,1.3 Multijet Pop,2017,149900,DÃ¼z,Dizel,Sedan,1248.00000,95,Ã–nden Ã‡ekiÅŸ,4.90000,45,1 deÄŸiÅŸen,Takasa Uygun,Galeriden]
#lr.predict(feaet)
df = pd.read_csv('final_df.csv')
print('\nNumber of rows and columns in the data set: ',df.shape)

def dummies(dataFrame):
    df_1 = pd.get_dummies(dataFrame["Vites Tipi"])
    df_2 = pd.get_dummies(dataFrame["YakÄ±t Tipi"])
    df_3 = pd.get_dummies(dataFrame["Kasa Tipi"])
    df_4 = pd.get_dummies(dataFrame["Ã‡ekiÅŸ"])
    df_5 = pd.get_dummies(dataFrame["Takasa Uygun"])
    df_6 = pd.get_dummies(dataFrame["Kimden"])

    dataFrame.drop('Vites Tipi', inplace=True, axis=1)
    dataFrame.drop('YakÄ±t Tipi', inplace=True, axis=1)
    dataFrame.drop('Kasa Tipi', inplace=True, axis=1)
    dataFrame.drop('Ã‡ekiÅŸ', inplace=True, axis=1)
    dataFrame.drop('Takasa Uygun', inplace=True, axis=1)
    dataFrame.drop('Kimden', inplace=True, axis=1)

    dataFrame = pd.concat([dataFrame, df_1], axis=1)
    dataFrame = pd.concat([dataFrame, df_2], axis=1)
    dataFrame = pd.concat([dataFrame, df_3], axis=1)
    dataFrame = pd.concat([dataFrame, df_4], axis=1)
    dataFrame = pd.concat([dataFrame, df_5], axis=1)
    dataFrame = pd.concat([dataFrame, df_6], axis=1)

    dataFrame.drop('-', inplace=True, axis=1)

    return dataFrame


df = dummies(df)
df.head()

print(df.Marka.unique())

# %%
plt.figure(figsize=(20,8))

plt.subplot(1,2,1)
plt.title('Car Price Distribution Plot')
sns.distplot(df["Price"])

plt.subplot(1,2,2)
plt.title('Car Price Spread')
sns.boxplot(y=df["Price"])

plt.show()


# %%
""" for our visualization purpose will fit line using seaborn library only for bmi as independent variable 
and charges as dependent variable"""
cmap = colors.ListedColormap(["#682F2F", "#9E726F", "#D6B2B1", "#B9C0C9", "#9F8A78", "#F3AB60"])
corrmat= df.corr()
plt.figure(figsize=(50,50))
sns.heatmap(corrmat,annot=True, cmap=cmap, center=0)
plt.show()


