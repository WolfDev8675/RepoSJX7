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
from sklearn import metrics as mtcs

#Loading the data
db=pd.read_csv("https://raw.githubusercontent.com/WolfDev8675/RepoSJX7/Assign5_miscellaneous/Task_GC_03/real_estate_price_size_year.csv")
print("\n\n Head of the database \n",db.head())
print("\n\n Information :\n");db.info();
print("\n\n Description :\n",db.describe())

#Data division 
X=db[["size","year"]].values #independent variables
Y=db[["price"]].values  #dependent variables 
X_train, X_test, y_train, y_test= tr_te_sp(X,Y, test_size=0.2, random_state=0)

#Model creation 
module=LinReg()
module.fit(X_train,y_train)

#Coefficients
coeffs=module.coef_
print("Coefficients: ",coeffs)
print("\n Equation of model: \n price=",coeffs[0,0],"* size + ",coeffs[0,1],"* year.")

#Predict Test results 
y_pred=module.predict(X_test)
#np.set_printoptions(precision=2)
#print(np.concatenate((y_pred.reshape(len(y_pred),1),y_test.reshape(len(y_test),1)),1))

#Evaluation of the Model
print("\n\n Error Evaluation ")
print(" Mean Absolute Error :: ",mtcs.mean_absolute_error(y_test,y_pred))
print(" Mean Squared Error  :: ",mtcs.mean_squared_error(y_test,y_pred))
print(" Root Mean Squared Error :: ",np.sqrt(mtcs.mean_squared_error(y_test,y_pred)))


#**
# ** End of code 
#** 
