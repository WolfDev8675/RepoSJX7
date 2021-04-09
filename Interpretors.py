#!usr/bin/python
 
#Code file: Interpretors.py
#Task: 
#**  Interpret the solution to the data

#imports 
import pandas as PD
import numpy as NP
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve
from sklearn.metrics import confusion_matrix,accuracy_score,precision_recall_fscore_support
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
    Precision=None
    Recall=None
    F_Score=None
    Support=None
    Specificity=None
    TN=None;TP=None;FN=None;FP=None;

    
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


    def generateMetrics(self,metricType='infos'):
        """ Function generateMetrics
            Parent Class: Logistic 
            Operation: Generate Metrics of the model  """
        self.PredictY=self.Model.predict(self.TestX)
        if metricType == 'info':
            self.confMatrix=confusion_matrix(self.TestY,self.PredictY)
            self.Accuracy=accuracy_score(self.TestY,self.PredictY)
            self.Precision,self.Recall,self.F_Score,self.Support=precision_recall_fscore_support(self.TestY,self.PredictY)
            self.TN,self.FP,self.FN,self.TP=self.confMatrix.ravel()
            self.Specificity=(self.TN*100)/(self.FP+self.TN)
            returnStr=""
            returnStr+= " True Positive Count : "+str(self.TP)+"\n"
            returnStr+= " True Negative Count : "+str(self.TN)+"\n"
            returnStr+= " False Positive Count : "+str(self.FP)+"\n"
            returnStr+= " False Negative Count : "+str(self.FN)+"\n"
            returnStr+= " Accuracy : "+str(self.Accuracy)+"\n"
            returnStr+= " Precision : "+str(self.Precision)+"\n"
            returnStr+= " Recall : "+str(self.Recall)+"\n"
            returnStr+= " Specificity : "+str(self.Specificity)+"\n"
            returnStr+= " Support : "+str(self.Support)+"\n"
            returnStr+= " F - Score : "+str(self.F_Score)+"\n"
            return returnStr

        elif metricType == 'plots':
            figure,(AXPCM,AXPROC)=PLOT.subplots(1,2,figsize=(13,7.5))
            figure.canvas.set_window_title(" Model Metrics  ")
            AXPCM=plot_confusion_matrix(self.Model,self.TestX,self.TestY)
            #AXPCM.figure_.set_title(" Confusion Matrix ")
            AXPROC=plot_roc_curve(self.Model,self.TestX,self.TestY)
            #AXPROC.figure_.set_title(" Receiver Operating Charactistics (ROC) ")
            #AXP.figure_.canvas.set_window_title(" Model Metrics  ")

            PLOT.show()
        

    def predictionApply(self,data):
        """ Function predictionApply
            Parent Class: Logistic 
            Operation:  Apply the trained Model on a different data 
            than on which it is trained or tested """
        return self.Model.predict(data)


    def retrainModel(self):
        """ Function retrain
            Parent Class: Logistic
            Operation: Retrain the previously generated model """
        self.generateModel()
        self.generateMetrics(metricType='plots')
