#!usr/bin/python

# imports
import numpy as NP
import pandas as PD
import matplotlib.pyplot as PLT
import seaborn as SNS
from sklearn.model_selection import train_test_split as tr_te_sp
from sklearn.model_selection import LinearRegression 

# import data 
data_B= PD.read_csv("e:\Source\Repos\WolfDev8675\RepoSJX7\Task_GC_01\Ecommerce Customers.csv - Ecommerce Customers.csv.csv")

#data _informations
print(" Dataset Head  ",data_B.head())
print(" Information ",data_B.info())
print(" Description ",data_B.describe())

# Exploratory Data analysis 

SNS.jointplot(x="Yearly Amount Spent",y="Time on Website",data=data_B);
SNS.jointplot(x="Yearly Amount Spent",y="Length of Membership",data=data_B);
SNS.pairplot(data_B)
A=data_B(data_B("Yearly Amount Spent","Length of Membership"))
g=SNS.FacetGrid(data=A,row="Yearly Amount Spent",col="Length of Membership");
g.map(SNS.scatterplot," Data details ")
PLT.show();

# Training and Testing Data
X=data_B.iloc[: -1:-1]
Y=data_B.iloc[:,-1]
X_train, X_test, y_train, y_test= tr_te_sp( test_size=0.3, random_state=101)