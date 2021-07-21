#!usr/bin/python

#Problem Statement:
# Solve by using Decision Trees the solution to the data given 

#imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier as DecTree
from sklearn.preprocessing import OneHotEncoder as OHEnc

#Import Data
dbs=pd.read_csv("e:\Source\Repos\WolfDev8675\RepoSJX7\Task_GC_04\data.csv")
print(" Head of the data \n",dbs.head(5))
print(" Info of Data : \n",dbs.info())

# Data distribution 
X=dbs.iloc[:,-1:-1]
y=dbs.iloc[:-1]

# One Hot Encoding to fit data 
ohec=OHEnc()
X_enc=ohec.fit(X)
Y_enc=ohec.fit(y)

# Decisions 
clfTree=DecTree()
clfTree.fit(X_enc,Y_enc)

# Tree Details
clfTree.plot_tree()
plt.show()



#..
# End of Code 
#.. 