# -*- coding: utf-8 -*-
"""Netflix  stock prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QTi5oiyU6FCvz-PfcxgNKvBnZgfBOivg
"""

pip install keras

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv(r"NFLX.csv")
df

df.describe()

df.info()

df.isnull().sum()

df.nunique()

df.duplicated().sum()

df.shape

df.head(10)

df['Date'].nunique()

from datetime import datetime
a =df['Date'].min()
b =df['Date'].max()
A1 = datetime.strptime(b, "%Y-%m-%d")
B2 = datetime.strptime(a, "%Y-%m-%d")
diff = B2-A1
print(f'Difference is {diff.days} days')

df['Date'] =  pd.to_datetime(df['Date'], format='%Y-%m-%d')
df.set_index('Date', inplace=True)
df.head()

df = df.resample('D').ffill().reset_index()
df['Date'].nunique()

plt.figure(figsize=(30,20))
plt.plot(df['Close'])
plt.show()

df

df["Close"].plot.hist(alpha=0.5)
plt.show()

train_df=df[:900]
test_df=df[900:]

train_df.head(10)

test_df.tail(10)

train=train_df.loc[:,["Open"]].values

len(train)

from sklearn.preprocessing import MinMaxScaler
Mn=MinMaxScaler(feature_range=(0,1))
train_scaled=Mn.fit_transform(train)

plt.plot(train_scaled)
plt.show()

x_train=[]
y_train=[]
timesteps=50
for i in range(timesteps,len(train_scaled)):
    x_train.append(train_scaled[i-timesteps:i,0])
    y_train.append(train_scaled[i,0])
x_train,y_train=np.array(x_train),np.array(y_train)

len(x_train)

len(y_train)

x_train=np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))

x_train

import seaborn as sns

dt=df.corr()
dt

sns.heatmap(dt,annot=True)
plt.show()

sns.countplot(x=df["Open"])
plt.show()

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units = 1))
model.compile(optimizer = 'adam', loss = 'mean_squared_error')
model.fit(x_train, y_train, epochs = 10, batch_size = 32)

dataset=pd.concat((train_df["Open"],test_df["Open"]), axis=0)
inputs= dataset[len(dataset)-len(test_df)-timesteps:].values.reshape(-1,1)
inputs=Mn.transform(inputs)

#prediction
x_test=[]
for i in range(timesteps,timesteps+len(test_df)):
    x_test.append(inputs[i-timesteps:i,0])
x_test=np.array(x_test)
x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))
predicted_stock_price=model.predict(x_test)
predicted_stock_price=Mn.inverse_transform(predicted_stock_price)#we had scaled between 0-1 data, inversing it

real_stock_price=test_df.loc[:,["Open"]].values

plt.figure(figsize=(10,5))
plt.plot(real_stock_price,color="red",label="Real Netflix Stock Price")
plt.plot(predicted_stock_price,color="blue",label="Predicted Netflix Stock Price")
plt.title("Netflix Stock Price Prediction")
plt.xlabel("Time")
plt.ylabel("Stock Price")
plt.legend()
plt.show()

