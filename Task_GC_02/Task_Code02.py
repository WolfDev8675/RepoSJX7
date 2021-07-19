#!usr/bin/python

# imports
import numpy as NP
import pandas as PD
import matplotlib.pyplot as PLT
import seaborn as SNS
from sklearn.model_selection import train_test_split as tr_te_sp
from sklearn.preprocessing import StandardScaler as Std_Sc
from sklearn.linear_model import LogisticRegression as Log_Reg 
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report,plot_confusion_matrix,roc_curve, roc_auc_score,auc
from sklearn.model_selection import cross_val_score


# import data 
data_B= PD.read_csv(r"e:\Source\Repos\WolfDev8675\RepoSJX7\Task_GC_02\advertising.csv")

#data _informations
print(" Dataset Head  ",data_B.head())
print(" Information ",data_B.info())
print(" Description ",data_B.describe())

# Exploratory Data analysis 

SNS.histplot(data_B,x='Age')
SNS.jointplot(x="Age",y="Area Income",data=data_B,kind='scatter');PLT.show();
SNS.jointplot(x="Age",y="Daily Time Spent on Site",data=data_B,kind='kde',color='r');PLT.show();
SNS.jointplot(y="Daily Internet Usage",x="Daily Time Spent on Site",data=data_B,kind='scatter',color='g');PLT.show();
SNS.pairplot(data_B);PLT.show();

#Parititioning the data into componenets 
X=data_B[['Daily Time Spent on Site', 'Age', 'Area Income','Daily Internet Usage', 'Male']]
y=data_B['Clicked on Ad']

# Dataset spliting 
X_train, X_test, y_train, y_test= tr_te_sp(X,y, test_size=0.25, random_state=0)

#Logistic Modeling 
model=Log_Reg(solver='lbfgs')
model.fit(X_train,y_train)

#Predictions
y_pred=model.predict(X_test)

# Metics study 
cnf_mat=confusion_matrix(y_test,y_pred)
print("Confusion Matix : \n",cnf_mat)
acc_sc=accuracy_score(y_test,y_pred)
print(" Accuracy Score : ",acc_sc)

#Predicted Probabilities 
y_score=model.predict_proba(X_test)[:,1]

# Classification Report
print(classification_report(y_test,y_pred))


#..
# End of Code 
#.. 