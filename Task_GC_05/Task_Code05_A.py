#!usr/bin/python

#Problem Statement:
#Convert the decision tree program to model Linear calcification and Random Forest and report  your observation
# Part problem: Using Perceptron Linear Classification model 

#imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import Perceptron as A_Neur
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.preprocessing import OneHotEncoder as OHEnc

#Import Data
dbs=pd.read_csv("https://raw.githubusercontent.com/WolfDev8675/RepoSJX7/Assign5_miscellaneous/Task_GC_05/data.csv")
print("\n\n Head of the data \n",dbs.head(5));
print("\n\n Info of Data : \n");dbs.info();

# Data conversion 
dbs['Class']=dbs['Class'].astype('category') # Converting classifier field to categorical

# Data distribution 
print("\n\n Segregating  Data to the dependent and independent types ....")
X=dbs[["Gender","Car Type","Shirt Size"]]  # Independent variables 
y=dbs["Class"].cat.codes  # Dependent variables (categorical coded)

# One Hot Encoding to fit data 
print("\n Encoding ....")
ohec=OHEnc()
X_enc=ohec.fit_transform(X)

# Perceptrons 
print("\n Creating the Perceptron Linear model and training .... ")
neurs=A_Neur()
neurs.fit(X_enc,y) 

# Results
print("\n Score level achieved of the Perceptron Linear model ")
print("Score : ",neurs.score(X_enc,y))
