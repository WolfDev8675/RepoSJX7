#!usr/bin/python

# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.tree import DecisionTreeRegressor


# Code ....
# 
 
#Load dataset
dataset=pd.read_csv("e:\Source\Repos\WolfDev8675\RepoSJX7\Task4\Position_Salaries.csv")
X=dataset.iloc[:,1:-1].values
y=dataset.iloc[:,-1].values

print (X)
print(y)

#
regressor=DecisionTreeRegressor(random_state=0)
regressor.fit(X,y)
print(regressor.predict([[6.5]]))

X_grid=np.arange(min(X),max(X),0.01)
X_grid=X_grid.reshape((len(X_grid),1))
print(X_grid)
