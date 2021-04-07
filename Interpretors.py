#!usr/bin/python
 
#Code file: Interpretors.py
#Task: 
#**  Interpret the solution to the data

#imports 
import pandas as PD
import numpy as NP
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,plot_confusion_matrix
import matplotlib.pyplot as PLOT

#start of codes
class Logistic():
    """ class Logistic  """
     
    Model=None
    predictors=None
    inferences=None
    SplitRatio=None
    StudyData=None
    confMatrix=None
    TrainX=None;TestX=None;TrainY=None;TestY=None;PredictY=None
    Accuracy=None;

    
    def __init__(self,**kwargs):
        """ Class Logistic 
            Operation: create Logistic Regression Classifier Object """
        self.Model=LogisticRegression()
        for var in kwargs:
            if hasattr(self.Model,var):
                setattr(self.Model,var,kwargs[var])
            
    def pushData(self,dFrame=None,XHeads=None,YHeads=None):
        """ Function pushData:
            Parent Class: Logistic
            Operation: push the required data to the classifier model """
        self.StudyData=dFrame
        self.predictors=XHeads
        self.inferences=YHeads

    def generateModel(self):
        """ Function generateModel
            Parent Class: Logistic 
            Operation: Generate the respective Logistic Regression classifier model 
            from the data provided to the classifier object itself """
        R=self.SplitRatio
        testfactor=abs(((1/R)-1)/((1/R)-R))
        X=self.StudyData[self.predictors]
        Y=self.StudyData[self.inferences]
        self.TrainX,self.TestX,self.TrainY,self.TestY=train_test_split(X,Y,test_size=testfactor,random_state=0)
        self.Model.fit(self.TrainX,self.TrainY)


    def generateMetrics(self):
        """ Function generateMetrics
            Parent Class: Logistic 
            Operation: Generate confusion matrix """
        self.PredictY=self.Model.predict(self.TestX)
        self.confMatrix=confusion_matrix(self.TestY,self.PredictY)
        AXP=plot_confusion_matrix(self.Model,self.TestX,self.TestY)
        AXP.figure_.canvas.set_window_title(" Confusion Matrix ")
        PLOT.show()

    def predictionApply(self,data):
        """ Function predictionApply
            Parent Class: Logistic 
            Operation:  Apply the trained Model on a different data 
            than on which it is trained or tested """
        return self.Model.predict(data)


