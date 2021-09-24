#!usr/bin/python

""" Module for all Machine Learning models used in this Project """

# imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn import metrics #@post-analysis
import matplotlib.pyplot as plots  #@visuals



class Forecaster():
    """ Class Forecaster 
    target operation: Forcast with machine learning models,
        the nature of data fluctuations in a stock price dataset. """

    # variables 
    model=None
    predicts=None
    infers=None
    data=None
    XData=None
    YData=None
    split_data=None
    metric=None

    def __init__(self, model, **kwargs):
        """ Class Forcaster 
         creates a forcasting model 
        
         prameters: 
        model : the class of forcasting model 
        other parameters are with regards to specific variables in those classes """

        self.model=model
        for var in kwargs:
            if hasattr(self.model,var):
                setattr(self.model,var,kwargs[var])

            # end of init
    
    def pushData(self,data,predicts,infers):
        """ Input the data that the model will use to train 
            parameters---
            data: pandas.DataFrame object 
            predicts: list of field names used as predictors 
            infers: list of field name """

        
        if type(data) is not pd.DataFrame:
            raise TypeError(" data must be a pandas.DataFrame type object ")
        if type(predicts) is not list:
            raise TypeError(" predicts must be a list datatype ")
        self.data=data
        self.predicts=predicts
        if type(infers) is list:
            self.infers=infers[0]
        elif type(infers) is str:
            self.infers=infers
        else:
            raise TypeError(" infers must be a list or string datatype ")
        self.XData=self.data[self.predicts]
        self.YData=self.data[self.infers]

        #end of pushData

    def normal_split(self):
        """ Trains the forecasting model """ 
        X_train,X_test,y_train,y_test=train_test_split(self.XData,self.YData,test_size=0.3,random_state=0)
        self.split_data={'Train':{'x':X_train,'y':y_train},'Test':{'x':X_test}}
        

    def crossval_KF_split(self, **kwargs):
        """ Creates the training and testing sets on K fold cross validation """
        CrsV=KFold();
        for var in kwargs:
            if hasattr(CrsV,var):
                setattr(CrsV,var,kwargs[var])
        if [self.XData,self.YData] is not [None,None]:
            for train_index, test_index in CrsV.split(self.XData):
                X_train,X_test=self.XData.iloc[train_index],self.XData.iloc[test_index]
                y_train,y_test=self.YData.iloc[train_index],self.YData.iloc[test_index]
            self.split_data={'Train':{'x':X_train,'y':y_train},'Test':{'x':X_test}}
        else:
            raise ValueError(" No X,Y definition found ")
        
    def train(self):
        """ Trains the model on given data """
        self.model.fit(self.split_data['Train']['x'],self.split_data['Train']['y'])

    def plotMetrics(self,title="Model: unspecified"):
        """ Plots variation of the trained data """
        anotStr1='\n'.join((r"Mean Absolute Error: %f"%metrics.mean_absolute_error(self.YData,self.model.predict(self.XData)),
        r" Mean Squared Error:  %f"%metrics.mean_squared_error(self.YData,self.model.predict(self.XData)),
        r" Root Mean Squared Error:  %f"%np.sqrt(metrics.mean_squared_error(self.YData,self.model.predict(self.XData)))))
        predLR=self.model.predict(self.data[['Open','High','Low']])
        Fig1=plots.figure(figsize=(15,7.5));ax1=Fig1.add_subplot(111);
        plots.plot(self.data.index,self.data[[self.infers]])
        plots.plot_date(self.data.index,predLR,'g.-')
        plots.text(0.12,0.95,anotStr1,horizontalalignment='center',
            verticalalignment='center', transform=ax1.transAxes)
        plots.title(title)
        plots.show()
