#!usr/bin/python

#Problem Statement:
# Solve by using Decision Trees the solution to the data given 

#imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier as DecTree

#Import Data
dbs=pd.read_csv("e:\Source\Repos\WolfDev8675\RepoSJX7\Task_GC_04\data.csv")
print(" Head of the data \n",dbs.head(5))
print(" Info of Data : \n",dbs.info())

# Data distribution 
X=dbs.iloc[:,-1:-1]
y=dbs.iloc[:-1]
