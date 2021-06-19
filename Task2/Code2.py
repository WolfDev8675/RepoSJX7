#!usr/bin/python

# imports
import numpy as NP
import pandas as PD
import matplotlib.pyplot as PLT
import copy as CP
from sklearn.model_selection import train_test_split as tr_te_sp
from sklearn.linear_model import LinearRegression as LinReg
from sklearn import metrics 

# Code ....
# 
 
#Load dataset
dataset_raw=PD.read_csv("e:\Source\Repos\WolfDev8675\RepoSJX7\Task2\\50_Startups.csv")
dataset=CP.deepcopy(dataset_raw)

# details
dataset.info()
dataset.describe()

# changing the values of columns (** inkeep=true)
dataset.loc[dataset.State=='New York']=0
dataset.loc[dataset.State=='California']=1
dataset.loc[dataset.State=='Florida']=2

#converting the datatype of state to integer 
dataset['State']=dataset['State'].astype('int')

# ** alternative 
# from sklearn.compose import ColumnTransformer
# from Sklearn.preprocessing import OneHotEncoder 
# ct=ColumnTransformer(transformers=[('encoder',OneHotEncoder(){3})],remainder='passthrough')
# X=np.array(ct.fit_transform(X))
# 

# segmenting
X=dataset.iloc[:,:-1].values
Y=dataset.iloc[:-1].values

#check 
print("X: \n",X)
print("Y: \n",Y)

# Dataset spliting 
X_train, X_test, y_train, y_test= tr_te_sp(X,Y, test_size=1/3, random_state=0)

# Training Simple Linear Regression on training set 
regressor=LinReg()
regressor.fit(X_train,y_train)

y_pred=regressor.predict(X_test)
