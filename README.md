# RepoSJX7
Project 1: Email Marketing / Retail Propensity Modelling

Data Set: OnlineRetail as received from Kaggle

Data Length: 10,48,575
.
Fields to be considered: CustID, Quantity, Price, Invoice Date, Country and Stock Code.
X variables: Count, Recency, Quantity, Price, Country
Y variable: IF(Count > 2,1,0)

Problem Statement: 
Find out the probability of buying a specific stock on 15-April-2011 for a Customer. If the probability is greater than 0.8, then we email the Customer. 
Workaround:
Build the Logistics Regression model on data of 4147 Customers. Freeze the coefficients. 
Use those coefficients to predict Y for remaining 1777 Customers. 
Expected Output:
Performance Metrics of the Model.
Based on recency, who are the hot prospects. (out of 1777 Customers)
Based on probability, create 5 group of prospects who are to be targeted with Group 1 should consists of highest probability prospects. (On 1777 Customers)

