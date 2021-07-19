#!usr/bin/python

#imports
import pandas as pd




#start of code

#import of Data
dataB=pd.read_csv("e:\Source\Repos\WolfDev8675\RepoSJX7\Task_GC_01\Task5\WA_Fn-UseC_-HR-Employee-Attrition.csv")

#Informations
print(dataB.info())
print(" Description ", dataB.describe())