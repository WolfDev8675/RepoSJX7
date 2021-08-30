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
%matplotlib inline
import matplotlib.pyplot as PLT
import seaborn as SNS
from sklearn.model_selection import train_test_split as tr_te_sp
from sklearn.linear_model import LinearRegression as LineReg
from sklearn import metrics as mtcs


# import data 
data_B= PD.read_csv("https://raw.githubusercontent.com/WolfDev8675/RepoSJX7/Assign5_miscellaneous/Task_GC_01/Ecommerce%20Customers.csv%20-%20Ecommerce%20Customers.csv.csv")

#data _informations
print(" Dataset Head  ",data_B.head())
print(" Information ",data_B.info())
print(" Description ",data_B.describe())

# Exploratory Data analysis 

print("\n\nYearly Amount Spent vs. Time on Website")
SNS.jointplot(y="Yearly Amount Spent",x="Time on Website",data=data_B);PLT.show();
print("\n\nYearly Amount Spent vs. Time on App")
SNS.jointplot(y="Yearly Amount Spent",x="Time on App",data=data_B);PLT.show();
print("\n\nTime on App vs. Length of Membership")
SNS.jointplot(x="Time on App",y="Length of Membership",data=data_B,kind="hex");PLT.show();
print("\n\n Pair Plots of data correlations ")
SNS.pairplot(data_B);PLT.show();
print("\n\nYearly Amount Spent vs. Length of Membership")
SNS.lmplot(y="Yearly Amount Spent",x="Length of Membership",data=data_B);PLT.show();


# Training and Testing Data
X=data_B[['Avg. Session Length','Time on App','Time on Website','Length of Membership']]
Y=data_B['Yearly Amount Spent']
X_train, X_test, y_train, y_test= tr_te_sp(X,Y, test_size=0.3, random_state=101)

#Model creation 
lm=LineReg()
lm.fit(X_train,y_train)

#Coefficients
coeffs=lm.coef_
print("\n\nCoefficients: ",coeffs)

#Predict Test results 
y_pred=lm.predict(X_test)

#Visual of Prediction 
print("\n\n Predicted Values vs True Values ")
SNS.scatterplot(y_pred,y_test);PLT.show();print("\n\n")

#Evaluation of the Model
print(" Mean Absolute Error :: ",mtcs.mean_absolute_error(y_test,y_pred))
print(" Mean Squared Error  :: ",mtcs.mean_squared_error(y_test,y_pred))
print(" Root Mean Squared Error :: ",NP.sqrt(mtcs.mean_squared_error(y_test,y_pred)))

#Residuals 
residuals=y_test - y_pred;
print("\n\n Residuals ")
SNS.displot(residuals,kde=True);PLT.show()


#Conclusion 
print("\n\n \t \t Coefficients ")
print(" Avg. Session Length ",coeffs[0])
print(" Time on App  ",coeffs[1])
print(" Time on Website ",coeffs[2])
print(" Length of Membership ",coeffs[3])




#..
# End of Code 
#..
