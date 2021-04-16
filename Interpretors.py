#!usr/bin/python
 
#Code file: Interpretors.py
#Task: 
#**  Interpret the solution to the data

#imports 
import io
import pandas as PD
import numpy as NP
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score,roc_auc_score
import matplotlib.pyplot as PLOT

#start of codes
class Learner():
    """ class Learner  """
     
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
    Specificity=None
    TN=None;TP=None;FN=None;FP=None;
    ROC_AUC_Score=None

    
    def __init__(self,model,**kwargs):
        """ Class Learner
            Operation: create Machine Learning Classifier Object """

        self.Model=model
        for var in kwargs:
            if hasattr(self.Model,var):
                setattr(self.Model,var,kwargs[var])
      #end of iniitalizer function 
            
    def pushData(self,dFrame=None,XHeads=None,YHeads=None):
        """ Function pushData:
            Parent Class: Logistic
            Operation: push the required data to the classifier model """
        self.StudyData=dFrame
        self.predictors=XHeads
        self.inferences=YHeads
     #end of function

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
      #end of function


    def generateMetricsInfo(self):
        """ Function generateMetrics
            Parent Class: Logistic 
            Operation: Generate Metrics informations of the model  """
        buffer=io.StringIO()
        self.PredictY=self.Model.predict(self.TestX)
        self.confMatrix=confusion_matrix(self.TestY,self.PredictY)
        self.Accuracy=accuracy_score(self.TestY,self.PredictY)*100
        self.Precision=precision_score(self.TestY,self.PredictY)*100
        self.Recall=recall_score(self.TestY,self.PredictY)*100
        self.F_Score=f1_score(self.TestY,self.PredictY)*100
        self.TN,self.FP,self.FN,self.TP=self.confMatrix.ravel()
        self.Specificity=(self.TN*100)/(self.FP+self.TN)
        self.ROC_AUC_Score=roc_auc_score(self.TestY,self.PredictY)
        buffer.write(" METRICS DETAILS \n")
        buffer.write(" True Positive Count : "+str(self.TP)+"\n\n")
        buffer.write(" True Negative Count : "+str(self.TN)+"\n\n")
        buffer.write(" False Positive Count : "+str(self.FP)+"\n\n")
        buffer.write(" False Negative Count : "+str(self.FN)+"\n\n\n\n")
        buffer.write(" Accuracy : "+str(self.Accuracy)+"\n\n")
        buffer.write(" Precision : "+str(self.Precision)+"\n\n")
        buffer.write(" Recall : "+str(self.Recall)+"\n\n")
        buffer.write(" Specificity : "+str(self.Specificity)+"\n\n")
        buffer.write(" F - Score : "+str(self.F_Score)+"\n\n")
        buffer.write(" ROC AUC Score : "+str(self.ROC_AUC_Score)+"\n\n")
        return buffer.getvalue()
     #end of function 

    def generateMetricsPlots(self):
        """ Function generateMetrics
            Parent Class: Logistic 
            Operation: Generate Metrics informations of the model  """
        figure,(AXPCM,AXPROC)=PLOT.subplots(1,2,figsize=(13,7.5))
        figure.canvas.set_window_title(" Model Metrics  ")
        plot_confusion_matrix(self.Model,self.TestX,self.TestY,ax=AXPCM)
        AXPCM.set_title(" Confusion Matrix ")
        plot_roc_curve(self.Model,self.TestX,self.TestY,ax=AXPROC)
        AXPROC.set_title(" Receiver Operating Charactistics (ROC) ")
        PLOT.show()
      #end of function   

    def predictionApply(self,data):
        """ Function predictionApply
            Parent Class: Logistic 
            Operation:  Apply the trained Model on a different data 
            than on which it is trained or tested """
        return self.Model.predict(data)
       #end of function

    def retrainModel(self):
        """ Function retrain
            Parent Class: Logistic
            Operation: Retrain the previously generated model """
        self.generateModel()
        self.generateMetricsPlots()
    #end of function 

 #end of class: Logistic

 #END OF FILE 'Interpretors.py'