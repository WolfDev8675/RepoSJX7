#!usr/bin/python
 
#Code file: Interpretors.py
#Task: 
#**  Interpret the solution to the data

#imports 
import pandas as PD
import numpy as NP
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

#start of codes
class Logistic():
    """ class Logistic  """
    Model=None
    predictors=None
    inferences=None
    SplitRatio=None
    StudyData=None
    confMatrix=None

    def __init__(self):
        self.Model=LogisticRegression()

    
    def generateModel(self):
        """ function """
        R=self.SplitRatio
        testfactor=abs(((1/R)-1)/(1/R)-R)
        X=data[predictors]
        Y=data[inferences]
        X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=testfactor,random_state=0)
        self.Model.fit(X_train,y_train)

    def generateMetrics(self):
        """function"""
        y_pred=self.Model.predict(X_test)
        self.confMatrix=confusion_matrix(y_test, y_pred)

    def prediction(self,data):
        """ function """
        return self.Model.predict(data)


