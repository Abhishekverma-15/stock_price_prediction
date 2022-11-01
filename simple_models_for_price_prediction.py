# -*- coding: utf-8 -*-
"""Simple models for price prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e3oYa5vo-0EyhpubLDZqH_Ul-SbtU5BX
"""

import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
plt.style.use('bmh')

stock = 'INFY'

df = web.DataReader(stock,data_source = "yahoo" , start = "2020-01-01",end='2021-05-05')

#df = df['Close']    # gives you a panda series object
df = df[['Close','Volume']] #gives you a pandas data frame
df.head()

#   how many days ahead you want to predict
forecast_out = 15

df['Prediction'] = df[['Close']].shift(-forecast_out);
df

#data processing

x = np.array(df[['Close',"Volume"]])[ :-forecast_out]    # use df[['Close','Volume','SMA20']] to include other features
y = np.array(df['Prediction'])[ : -forecast_out]

xtrain,xvalid,ytrain,yvalid = train_test_split(x,y,test_size = 0.2)

xfinal = np.array(df[['Close','Volume']])[-forecast_out : ]

ytrue = web.DataReader(stock,data_source = "yahoo" , start = "2021-05-06",end='2021-05-30')
ytrue = ytrue[:forecast_out]

#print(x[:5])

# train and test Support Vector Machine (Regressor)

'''
C : Regularization parameter. The strength of the regularization is inversely proportional to C.
The penalty is a squared l2 penalty.

The parameter C, common to all SVM kernels, trades off misclassification of training examples against simplicity of the decision surface. 
A low C makes the decision surface smooth, while a high C aims at classifying all training examples correctly. 

gamma defines how much influence a single training example has. The larger gamma is, the closer other examples must be to be affected.

svr_score() returns coefficient of determination (r^2) : 
r^2 : describes what % of variation in y comes from variation in x and not from  variation from fitted plane
'''

# SVM without volumes here, does better than with volumes

'''
# Grid Search

c = 0.0001

while c <= 1e5:
    g = 0.0001
    while g <= 1e5:

        svr_rbf = SVR(kernel = 'rbf', C = c , gamma = g)
        svr_rbf.fit(xtrain[:,:-1],ytrain)
        svm_confidence = svr_rbf.score(xvalid[:,:-1],yvalid)
        print('svm confidence : ',svm_confidence,' ',c,' ',g)
        g *= 10
    c *= 10

'''
c = 1000
g = 0.001

# dropping the volumes

svr_rbf = SVR(kernel = 'rbf', C = c , gamma = g)
svr_rbf.fit(xtrain[:,:-1],ytrain)
svm_confidence = svr_rbf.score(xvalid[:,:-1],yvalid)
print('svm confidence : ',svm_confidence)

svr_prediction = svr_rbf.predict(xfinal[:,:-1])
ytrue['Prediction'] = svr_prediction
plt.figure(figsize=(16, 8))
plt.title('SVR without volumes Model')
plt.xlabel('Days')
plt.ylabel('Close Price')
plt.plot(df['Close'])
plt.plot(ytrue[['Close', 'Prediction']])
plt.legend(['Orig', 'Valid', 'Pred'])
plt.show()

# SVM with volumes here, does not do well at all
scalar = MinMaxScaler(feature_range=(0,1))

newxtrain = scalar.fit_transform(xtrain)
newxvalid = scalar.fit_transform(xvalid)
newxfinal = scalar.fit_transform(xfinal)



# # Grid Search

# c = 0.0001

# while c <= 1e5:
#     g = 0.0001
#     while g <= 1e5:

#         svr_rbf = SVR(kernel = 'rbf', C = c , gamma = g)
#         svr_rbf.fit(newxtrain,ytrain)
#         svm_confidence = svr_rbf.score(newxvalid,yvalid)
#         print('svm confidence : ',svm_confidence,' ',c,' ',g)
#         g *= 10
#     c *= 10





c = 1000
g = 0.01
svr_rbf = SVR(kernel = 'rbf', C = c , gamma = g)
svr_rbf.fit(newxtrain,ytrain)

svr_prediction = svr_rbf.predict(newxfinal)


#svr_prediction = svr_rbf.predict(xfinal[:,:-1])


ytrue['Prediction'] = svr_prediction
plt.figure(figsize=(16, 8))
plt.title('SVR with volumes Model')
plt.xlabel('Days')
plt.ylabel('Close Price')
plt.plot(df['Close'])
plt.plot(ytrue[['Close', 'Prediction']])
plt.legend(['Orig', 'Valid', 'Pred'])
plt.show()

#data processing

x = np.array(df[['Close',"Volume"]])[ :-forecast_out]    # use df[['Close','Volume','SMA20']] to include other features
y = np.array(df['Prediction'])[ : -forecast_out]

xtrain,xvalid,ytrain,yvalid = train_test_split(x,y,test_size = 0.2)

xfinal = np.array(df[['Close','Volume']])[-forecast_out : ]

ytrue = web.DataReader(stock,data_source = "yahoo" , start = "2021-05-06",end='2021-05-30')
ytrue = ytrue[:forecast_out]

# (Multiple) Linear Regression here

lr = LinearRegression()
lr.fit(xtrain,ytrain)

print(lr.coef_)

lr_confidence = lr.score(xvalid,yvalid)
print('lr confidence : ',lr_confidence)

lr_prediction = lr.predict(xfinal)
lr_prediction

ytrue['Prediction'] = lr_prediction
plt.figure(figsize=(16, 8))
plt.title('LR Model')
plt.xlabel('Days')
plt.ylabel('Close Price')
plt.plot(df['Close'])
plt.plot(ytrue[['Close', 'Prediction']])
plt.legend(['Orig', 'Valid', 'Pred'])
plt.show()