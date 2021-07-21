#!usr/bin/python

#Problem Statement:
#You are given a real estate dataset.

#Real estate is one of those examples that every regression course goes through as it is extremely 
#easy to understand and there is a (almost always) certain causal relationship to be found.

#The data is located in the file: 'real_estate_price_size_year.csv'.

#You are expected to create a multiple linear regression (similar to the one in the lecture), using the new data.

#In this exercise, the dependent variable is 'price', while the independent variables are 'size' and 'year'.
#..

#imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split as tr_te_sp
from sklearn.linear_model import LinearRegression as LinReg
from sklearn.metrics import confusion_matrix,accuracy_score

#Loading the data
db=pd.read_csv(r"e:\Source\Repos\WolfDev8675\RepoSJX7\Task_GC_03\real_estate_price_size_year.csv")
print("Head of the database \n",db.head())
print(" Information :\n",db.info())
print(" Description :\n",db.describe())

#Data division 
X=db(["size","year"]).values
Y=db(["price"]).values
X_train, X_test, y_train, y_test= tr_te_sp(X,Y, test_size=0.2, random_state=0)

#Model creation 
module=LinearRegression
module.fit(X_train,y_train)

#Coefficients
coeffs=module.coef_
print("Coefficients: ",coeffs)

#Predict Test results 
y_pred=module.predict(X_test)

# Metics study 
cnf_mat=confusion_matrix(y_test,y_pred)
print("Confusion Matix : \n",cnf_mat)
acc_sc=accuracy_score(y_test,y_pred)
print(" Accuracy Score : ",acc_sc)
