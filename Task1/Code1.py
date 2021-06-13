#!usr/bin/python

# imports
import numpy as NP
import pandas as PD
import matplotlib.pyplot as PLT
from sklearn.model_selection import train_test_split as tr_te_sp
from sklearn.linear_model import LinearRegression as LinReg
from sklearn import metrics 

# Code ....
# 
 
#Load dataset
dataset=PD.read_csv("e:\Source\Repos\WolfDev8675\RepoSJX7\Task1\Salary_Data.csv")
print(dataset.head(20))  

dataset.info()
X=dataset.iloc[:,:-1].values #Storing value of YearsExperience in Variable X
print(X)
Y=dataset.iloc[:,-1].values #Storing value of salary in Variable Y 
print(Y)

# Dataset spliting 
X_train, X_test, y_train, y_test= tr_te_sp(X,Y, test_size=1/3, random_state=0)
print(X_train)
print(X_test)
print(y_train)

print("x_train",len(X_train))
print("y_train",len(y_train))
# Training Simple Linear Regression on training set 
regressor=LinReg()
regressor.fit(X_train,y_train)

# Prediction using test 
y_pred=regressor.predict(X_test)

# Visualising the Training set results
PLT.scatter(X_train, y_train, color = 'red')
PLT.plot(X_train, regressor.predict(X_train), color = 'blue')
PLT.title('Salary vs Experience (Training set)')
PLT.xlabel('Years of Experience')
PLT.ylabel('Salary')
PLT.show() 

# Visualising the Test set results
PLT.scatter(X_test, y_test, color = 'red')
PLT.plot(X_train, regressor.predict(X_train), color = 'blue')
PLT.title('Salary vs Experience (Test set)')
PLT.xlabel('Years of Experience')
PLT.ylabel('Salary')
PLT.show() 

#Printing the Intercept 
print(" intercept : ",regressor.intercept_)

print("MAE:  ",metrics.mean_absolute_error(y_test,y_pred))
print("MSE:  ",metrics.mean_squared_error(y_test,y_pred))
print("RMSE: ",NP.sqrt(metrics.mean_squared_error(y_test,y_pred)))

#end of code 