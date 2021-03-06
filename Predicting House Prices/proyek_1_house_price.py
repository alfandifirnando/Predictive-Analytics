# -*- coding: utf-8 -*-
"""Proyek 1 - House Price.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PULeQpne49H1N9IJYeBvfrX2tG3cznGS

# Proyek Machine Learning Prediksi Harga Rumah - Alfandi Firnando

## Data Loading

### Import library machine learning yang diperlukan
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
# %matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

"""### Connect dengan googgle drive untuk mengakses data"""

from google.colab import drive
drive.mount('/content/drive')

"""### Melakukan data loading dari directory"""

df = pd.read_csv('/content/drive/MyDrive/kc_house_data.csv')
df.head()

df.tail()

df.shape

df.info()

"""### Drop kolom yang informasinya tidak penting untuk prediksi harga rumah"""

df.drop(columns=["id", "date"], inplace=True)

df.info()

df.head()

df.describe()

df.shape

"""## Data Understanding

### Melakukan visualisasi terhadap data outliers
"""

sns.boxplot(x=df['bedrooms'])

sns.boxplot(x=df['bathrooms'])

sns.boxplot(x=df['sqft_living'])

"""### Melakukan penanganan terhadap data outliers"""

Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR=Q3-Q1
df=df[~((df<(Q1-1.5*IQR))|(df>(Q3+1.5*IQR))).any(axis=1)]
 
# Cek ukuran dataset setelah kita drop outliers
df.shape

"""### Melakukan visualisasi untuk melihat persebaran data"""

df.hist(bins=50, figsize=(20,15))
plt.show()

"""### Melakukan visualisasi correlation matrix untuk melihat korelasi antar feature"""

sns.pairplot(df, diag_kind = 'kde')

plt.figure(figsize=(10, 8))
correlation_matrix = df.corr().round(2)
 
# Untuk menge-print nilai di dalam kotak, gunakan parameter anot=True
sns.heatmap(data=correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, )
plt.title("Correlation Matrix untuk Fitur Numerik ", size=20)

"""## Data Preparation

### Melakukan drop kolom berdasarkan analisa dari correlation matrix
"""

df.drop(['long', 'zipcode', 'yr_built', 'yr_renovated', 'condition', 'waterfront', 'view'], inplace=True, axis=1)

df.head()

df.shape

"""### Train Test Split :

membagi dataset menjadi data latih (train) dan data uji (test) dengan perbandingan 80:20.
"""

X = df.drop(columns="price")
y = df.price

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

X_train.columns

"""### Standarisasi

Selanjutnya saya melakukan standarisasi membantu untuk membuat fitur data menjadi bentuk yang lebih mudah diolah oleh algoritma.
"""

from sklearn.preprocessing import StandardScaler
 
numerical_features = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'grade', 'sqft_above', 'sqft_basement', 'lat', 'sqft_living15', 'sqft_lot15']
scaler = StandardScaler()
scaler.fit(X_train[numerical_features])
X_train[numerical_features] = scaler.transform(X_train.loc[:, numerical_features])
X_train[numerical_features].head()

"""## Modeling

Menggunakan model regresi machine learning yaitu KNN dan Random Forest
"""

models = pd.DataFrame(index=['train_mse', 'test_mse'], 
                      columns=['KNN', 'RandomForest'])

"""### Model KNN"""

from sklearn.neighbors import KNeighborsRegressor
 
knn = KNeighborsRegressor(n_neighbors=3)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_train)

"""### Model Random Forest"""

# Impor library yang dibutuhkan
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
 
# buat model prediksi
RF = RandomForestRegressor(n_estimators=50, max_depth=16, random_state=55, n_jobs=-1)
RF.fit(X_train, y_train)
 
models.loc['train_mse','RandomForest'] = mean_squared_error(y_pred=RF.predict(X_train), y_true=y_train)

X_test.loc[:, numerical_features] = scaler.transform(X_test[numerical_features])

"""## Evaluation

### Melakukan evaluasi dengan metrik MSE
"""

# Buat variabel mse yang isinya adalah dataframe nilai mse data train dan test pada masing-masing algoritma
mse = pd.DataFrame(columns=['train', 'test'], index=['KNN','RF'])
 
# Buat dictionary untuk setiap algoritma yang digunakan
model_dict = {'KNN': knn, 'RF': RF}
 
# Hitung Mean Squared Error masing-masing algoritma pada data train dan test
for name, model in model_dict.items():
    mse.loc[name, 'train'] = mean_squared_error(y_true=y_train, y_pred=model.predict(X_train))/1e3 
    mse.loc[name, 'test'] = mean_squared_error(y_true=y_test, y_pred=model.predict(X_test))/1e3
 
# Panggil mse
mse

"""### Visualisai dari 2 model yang sudah dievaluasi"""

fig, ax = plt.subplots()
mse.sort_values(by='test', ascending=False).plot(kind='barh', ax=ax, zorder=3)
ax.grid(zorder=0)