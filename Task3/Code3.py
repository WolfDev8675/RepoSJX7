#!usr/bin/python

# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split as tr_te_sp
from sklearn.preprocessing import StandardScaler as Std_Sc
from sklearn.linear_model import LogisticRegression as Log_Reg 
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report,plot_confusion_matrix,roc_curve, roc_auc_score,auc
from sklearn.model_selection import cross_val_score

# Code ....
# 
 
#Load dataset
dataset=pd.read_csv("e:\Source\Repos\WolfDev8675\RepoSJX7\Task3\Social_Network_Ads.csv")
X=dataset.iloc[:,:-1].values
y=dataset.iloc[:,-1].values

#check1
print(dataset.head())
print("X: ",X)
print("y: ",y)

# Dataset spliting 
X_train, X_test, y_train, y_test= tr_te_sp(X,y, test_size=0.25, random_state=0)

# check2
print(X_test)

# Feature Scaling 
sclr=Std_Sc()
X_train=sclr.fit_transform(X_train)
X_test=sclr.transform(X_test)

# check2
print(X_test)

# Model creation and training 
model=Log_Reg(random_state=0)
model.fit(X_train,y_train)

# check4 : Model fit accuracy
print(model.predict(sclr.fit_transform([[30,87000]])))

# Prediction 
y_pred=model.predict(X_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

# Metics study 
cnf_mat=confusion_matrix(y_test,y_pred)
print("Confusion Matix : \n",cnf_mat)
acc_sc=accuracy_score(y_test,y_pred)
print(" Accuracy Score : ",acc_sc)

#Predicted Probabilities 
y_score=model.predict_proba(X_test)[:,1]
print(y_score)

# Classification Report
print(classification_report(y_test,y_pred))
#plot_confusion_matrix(model,X_test,y_pred)
#plt.show()

# ROC details 
fpR,tpR,Thresh=roc_curve(y_test,y_score)

# ROC plot 
plt.title("Receiver Operating Characteristic (ROC)")
roc_auc=auc(fpR,tpR)
plt.plot(fpR,tpR,'b',label="AUC= %f"%roc_auc)
plt.legend(loc='lower right')
plt.plot([0,1],ls="--")
plt.plot([0,0],[1,0],c=".7")
plt.plot([1,1],c=".7")
plt.ylabel("True Positive Rate (TPR= TP/P = TP/(TP+FN)) ")
plt.xlabel("False Positive Rate (FPR= FP/N = FP/(FP+TN)) ")
plt.show()
