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
    X_train=None;X_test=None;y_train=None;y_test=None
    
    def __init__(self,**kwargs):
        self.Model=LogisticRegression()
        for var in kwargs:
            if hasattr(self.Model,var):
                setattr(self.Model,var,kwargs[var])
            
    
    def generateModel(self):
        """ function """
        R=self.SplitRatio
        testfactor=abs(((1/R)-1)/((1/R)-R))
        X=self.StudyData[self.predictors]
        Y=self.StudyData[self.inferences]
        self.X_train,self.X_test,self.y_train,self.y_test=train_test_split(X,Y,test_size=testfactor,random_state=0)
        self.Model.fit(self.X_train,self.y_train)

    def generateMetrics(self):
        """function"""
        y_pred=self.Model.predict(self.X_test)
        self.confMatrix=confusion_matrix(self.y_test, y_pred)

    def prediction(self,data):
        """ function """
        return self.Model.predict(data)


