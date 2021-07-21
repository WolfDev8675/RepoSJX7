#!usr/bin/python

#Problem Statement:
#You just got some contract work with an Ecommerce company based in New York City that sells clothing online 
#but they also have in-store style and clothing advice sessions. Customers come in to the store, have sessions/meetings 
#with a personal stylist, then they can go home and order either on a mobile app or website for the clothes they want.
#The company is trying to decide whether to focus their efforts on their mobile app experience or their website. 
#They've hired you on contract to help them figure it out! ..

# imports
import numpy as NP
import pandas as PD
import matplotlib.pyplot as PLT
import seaborn as SNS
from sklearn.model_selection import train_test_split as tr_te_sp
from sklearn.linear_model import LinearRegression 
from sklearn import metrics as mtcs


# import data 
data_B= PD.read_csv("e:\Source\Repos\WolfDev8675\RepoSJX7\Task_GC_01\Ecommerce Customers.csv - Ecommerce Customers.csv.csv")

#data _informations
print(" Dataset Head  ",data_B.head())
print(" Information ",data_B.info())
print(" Description ",data_B.describe())

# Exploratory Data analysis 

SNS.jointplot(x="Yearly Amount Spent",y="Time on Website",data=data_B);PLT.show();
SNS.jointplot(x="Yearly Amount Spent",y="Length of Membership",data=data_B);PLT.show();
SNS.pairplot(data_B);PLT.show();
#data_B("Length of Membership")=round(data_B("Length of Membership"))
#g=SNS.FacetGrid(data_B,row="Yearly Amount Spent");
#g.map(SNS.scatterplot," Data details ")
#PLT.show();

# Training and Testing Data
X=data_B.iloc[: -1:-1]
Y=data_B.iloc[:,-1]
X_train, X_test, y_train, y_test= tr_te_sp(X,Y, test_size=0.3, random_state=101)

#Model creation 
module=LinearRegression
module.fit(X_train,y_train)

#Coefficients
coeffs=module.coef_
print("Coefficients: ",coeffs)

#Predict Test results 
y_pred=module.predict(X_test)

#Visual of Prediction 
SNS.scatterplot(y_pred,y_test);PLT.show()

#Evaluation of the Model
print(" Mean Absolute Error :: ",mtcs.mean_absolute_error(y_test,y_pred))
print(" Mean Squared Error  :: ",mtcs.mean_squared_error(y_test,y_pred))
print(" Root Mean Squared Error :: ",NP.sqrt(mtcs.mean_squared_error(y_test,y_pred)))

#Residuals 
SNS.displot(data_B)

#Conclusion 
print(" \t \t Coefficients ")
print(" Avg. Session Length ",coeffs[0])
print(" Time on App  ",coeffs[1])
print(" Time on Website ",coeffs[2])
print(" Length of Membership ",coeffs[3])




#..
# End of Code 
#..