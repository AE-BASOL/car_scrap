#%%
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 04:18:20 2018

@author: Ahmet Basol
"""

#1. kutuphaneler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#2. Veri Onisleme

#2.1. Veri Yukleme
veriler = pd.read_csv('final_df.csv')
#pd.read_csv("veriler.csv")


#veri on isleme
aylar = veriler[['Price']]
#test
print(aylar)

satislar = veriler[['YÄ±l']]
print(satislar)


# %%verilerin egitim ve test icin bolunmesi
from sklearn.model_selection import train_test_split
x_train, x_test,y_train,y_test = train_test_split(aylar,satislar,test_size=0.33)

#verilerin olceklenmesi
from sklearn.preprocessing import StandardScaler


sc = StandardScaler()
X_train = sc.fit_transform(x_train)
X_test = sc.fit_transform(x_test)
Y_train = sc.fit_transform(y_train)
Y_test = sc.fit_transform(y_test)


print("asdas")
# model inşası (linear regression)
from sklearn.linear_model import LinearRegression




x_train = x_train.sort_index()
y_train = y_train.sort_index()

lr = LinearRegression()
lr.fit(x_train,y_train)

tahmin = lr.predict(x_test)

tahmin = pd.DataFrame(tahmin).sort_index()
y_test = y_test.sort_index()
print(tahmin)
plt.figure(figsize=(30, 10))
plt.title("Linear Model Result")
plt.plot(x_test, "-o")
plt.plot(tahmin, "-*")
plt.legend(["Pred", "Actual"])
plt.grid(True)
plt.show()

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)
print(tahmin.shape)
plt.plot(x_train,y_train)
plt.plot(x_test,tahmin)