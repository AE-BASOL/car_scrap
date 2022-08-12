# %%
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


import plotly.graph_objs as go
from plotly import tools
from plotly.subplots import make_subplots
import plotly.offline as py



# %%
df = pd.read_csv("final_df.csv")
print(df.head())
print(df.info())


print(df["Boya-deÄŸiÅŸen"].unique())

# %%
x = df.iloc[:,[0,7]].values #price ve yıl
#x = df.iloc[:,[0,8]].values #price ve kilometre
#x = df.iloc[:,[9,10]].values #motor hacmi ve motor gücü
#x = df.iloc[:,[8,11]].values #price ve ort yakıt

WCSS = []

for i in range(1,11):
    model = KMeans(n_clusters = i,init = 'k-means++')
    model.fit(x)
    WCSS.append(model.inertia_)

fig = plt.figure(figsize = (7,7))
plt.plot(range(1,11),WCSS, linewidth=4, markersize=12,marker='o',color = 'green')
plt.xticks(np.arange(11))
plt.xlabel("Number of clusters")
plt.ylabel("WCSS")
plt.show()

# %%
model = KMeans(n_clusters = 2, init = "k-means++", max_iter = 300, n_init = 10, random_state = 0)
y_clusters = model.fit_predict(x)

plt.figure(figsize = (20,10))
#plt.scatter(x[y_clusters == 2,0],x[y_clusters == 2,1],s = 50, c = 'red', label = "High")
plt.scatter(x[y_clusters == 0,0],x[y_clusters == 0,1],s = 50, c = 'green', label = "Medium")
plt.scatter(x[y_clusters == 1,0],x[y_clusters == 1,1],s = 50, c = 'blue', label = "Low")
#plt.scatter(x[y_clusters == 3,0],x[y_clusters == 3,1],s = 50, c = 'black', label = "Low")
#plt.scatter(x[y_clusters == 4,0],x[y_clusters == 4,1],s = 50, c = 'cyan', label = "Lowest Low")

plt.scatter(model.cluster_centers_[:,0],model.cluster_centers_[:,1], s = 100, c = "yellow", label = "centroids")
plt.xlabel("Price(kTL) -- >")
plt.ylabel("Year -- >")
plt.legend()
plt.show()

# %%
# input matrix for segmentation
x = df[['Price','Yıl','Ort. YakÄ±t TÃ¼ketimi']].values
# find the optimal number of clusters using elbow method  -- >This is for 3 features = [age,anual income,spending score]

WCSS = []

for i in range(1,11):
    model = KMeans(n_clusters = i,init = 'k-means++')
    model.fit(x)
    WCSS.append(model.inertia_)
fig = plt.figure(figsize = (7,7))
plt.plot(range(1,11),WCSS, linewidth=4, markersize=12,marker='o',color = 'red')
plt.xticks(np.arange(11))
plt.xlabel("Number of clusters")
plt.ylabel("WCSS")
plt.show()

# %%
# finding the clusters based on input matrix "x"
model = KMeans(n_clusters = 5, init = "k-means++", max_iter = 300, n_init = 10, random_state = 0)
y_clusters = model.fit_predict(x)
# countplot to check the number of clusters and number of customers in each cluster
sns.countplot(y_clusters)

# %%
fig = plt.figure(figsize = (15,15))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x[y_clusters == 0,0],x[y_clusters == 0,1],x[y_clusters == 0,2], s = 40 , color = 'blue', label = "cluster 0")
ax.scatter(x[y_clusters == 1,0],x[y_clusters == 1,1],x[y_clusters == 1,2], s = 40 , color = 'orange', label = "cluster 1")
ax.scatter(x[y_clusters == 2,0],x[y_clusters == 2,1],x[y_clusters == 2,2], s = 40 , color = 'red', label = "cluster 1")
ax.scatter(x[y_clusters == 3,0],x[y_clusters == 3,1],x[y_clusters == 3,2], s = 40 , color = 'green', label = "cluster 1")
ax.scatter(x[y_clusters == 4,0],x[y_clusters == 4,1],x[y_clusters == 4,2], s = 40 , color = 'black', label = "cluster 1")


ax.set_xlabel('Price -->')
ax.set_ylabel('Yıl --->')
ax.set_zlabel('Ort. Yakıt Tüketimi -->')
ax.legend()
plt.show()

# %%
# 3d scatterplot using plotly
Scene = dict(xaxis = dict(title  = 'Price -->'),yaxis = dict(title  = 'Yıl --->'),zaxis = dict(title  = 'Ort. Yakıt Tüketimi -->'))

labels = model.labels_
trace = go.Scatter3d(x=x[:, 0], y=x[:, 1], z=x[:, 2], mode='markers',marker=dict(color = labels, size= 5, line=dict(color= 'black',width = 1)))
layout = go.Layout(margin=dict(l=0,r=0),scene = Scene,height = 1000,width = 1000)
data = [trace]
fig = go.Figure(data = data, layout = layout)
fig.show()