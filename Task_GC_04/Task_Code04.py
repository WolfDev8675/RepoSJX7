#!usr/bin/python

#Problem Statement:
# Solve by using Decision Trees the solution to the data given 

#imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier as DecTree
from sklearn.tree import plot_tree
from sklearn.preprocessing import OneHotEncoder as OHEnc

#Import Data
dbs=pd.read_csv("https://raw.githubusercontent.com/WolfDev8675/RepoSJX7/Assign5_miscellaneous/Task_GC_04/data.csv")
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


# Decisions 
print("\n Creating the Tree model and training .... ")
clfTree=DecTree()
clfTree.fit(X_enc,y)

# Tree Details
print("\n\n Plot of the Finalized tree ")
fig=plt.figure();sbs=fig.add_subplot(111);
plot_tree(clfTree,class_names=['C0','C1'])
plt.show()



#..
# End of Code 
#.. 
