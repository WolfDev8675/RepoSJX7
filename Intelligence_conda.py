#!usr/bin/python

""" Module for handling all Machine Learning models used in this Project """

# imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold, GridSearchCV, RandomizedSearchCV
from sklearn import metrics 
import matplotlib.pyplot as plots  
from Visuals import residualsPlot


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
        self.split_data={'Train':{'x':X_train,'y':y_train},'Test':{'x':X_test,'y':y_test}}
        

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
            self.split_data={'Train':{'x':X_train,'y':y_train},'Test':{'x':X_test,'y':y_test}}
        else:
            raise ValueError(" No X,Y definition found ")
        
    def train(self):
        """ Trains the model on given data """
        self.model.fit(self.split_data['Train']['x'],self.split_data['Train']['y'])
    
    def train_full(self):
        """ Trains on the whole data """
        self.model.fit(self.XData,self.YData)

    def plotMetrics(self,data,title="Model: unspecified"):
        """ Plots variation of the trained data """
        XData=data[self.predicts]
        YData=data[self.infers]
        prediction=self.model.predict(XData)
        anotStr='\n'.join((r" Mean Absolute Error : %f".ljust(45,' ')%metrics.mean_absolute_error(YData,prediction),
        r" Mean Squared Error : %f".ljust(45,' ')%metrics.mean_squared_error(YData,prediction),
        r" Root Mean Squared Error : %f".ljust(45,' ')%np.sqrt(metrics.mean_squared_error(YData,prediction)),
        r" R{:} : %f".format('\xb2').ljust(45,' ')%metrics.r2_score(YData,prediction),
        r" Adjusted R{:} : %f".format('\xb2').ljust(45,' ')%(1-(1-metrics.r2_score(YData,prediction))*(len(YData)-1)/(len(YData)-XData.shape[1]-1)),
        r" Mean Absolute Percentage Error : %f".ljust(45,' ')%self.mean_absolute_percentage_error(YData,prediction)))
        Fig=plots.figure(figsize=(15,7.5));ax=Fig.add_subplot(111);
        plots.plot(data.index,data[[self.infers]])
        plots.plot_date(data.index,prediction,'g.-')
        plots.text(0.147,0.915,anotStr,horizontalalignment='center',
            verticalalignment='center', transform=ax.transAxes)
        plots.title(title)
        plots.show()

    def getThetas(self):
        """ Return the set of coefficients or thetas governing the model """
        C0=self.model.intercept_
        CN=self.model.coef_
        params=np.concatenate((np.array([C0]),CN))
        return params

    def cost_function(self,Xjs,Yjs,thetas):
        """ Calculate the Cost incurred of Error residues """
        
        phi_thetas=Yjs
        psi_theta=np.dot(Xjs,thetas)
        deltas=psi_theta-phi_thetas
        m=len(self.YData)
        cost=np.sum(np.square(deltas))*0.5/m
        return cost

    def grad_decent(self,alpha=0.01,iters=100):
        """ Use Gradient Decent method to purify model """
        m=len(self.YData)
        Xjs=np.c_[np.ones((len(self.XData),1)),self.XData]
        phi_thetas=self.YData
        thetas=self.getThetas()
        History={}
        for steps in range(iters):
            psi_theta=np.dot(Xjs,thetas)
            deltas=psi_theta-phi_thetas
            del_J_del_theta=Xjs.T.dot(deltas)/m
            thetas=thetas-alpha*del_J_del_theta
            History['Costs'][steps]=self.cost_function(Xjs=Xjs,Yjs=phi_thetas,thetas=thetas)
            History['Thetas'][steps]=thetas
        return History
        
    
    def gradientEnhanced(self,alpha=0.01,iters=100):
        """ Use Gradient descent functionality to provide an improved model"""
        History=self.grad_decent(alpha=alpha,iters=iters)
        minDeltaCost=min(History['Costs'].values)
        best_cost=0
        best_theta=0
        for i in iters:
            if History['Costs'][i]==minDeltaCost: 
                best_cost=History['Costs'][i]
                best_theta=History['Thetas'][i]
        self.model.intercept_=best_theta[0]
        self.model.coef_=best_theta[1:]
        self.metric={'ModelClass':type(self.model),'Best cost found':best_cost}
        return self.model

    def hyperboost(self,evaluator=GridSearchCV,**kwargs):
        """ Variable boosting for model improvement using 
        process of Hyperparameter Boost 
        this is applicable for only the Vector Machines and Ensemble Forest methods 
        *********************
        Variables 
        ---------------------
        evaluator : GridSearchCV (default) also usable is RandomizedSearchCV 
        **kwargs : all settings that are applicable to be used in the evaluator algorithm 
        -----------------------
        returns estimator model 
        (Created specifically with RandomForestRegressor and SupportVectorRegressor 
         other algorithms may be used if behaviour matches similar patterns)
        _______________________
        """
        worker=evaluator(estimator=self.model);
        for var in kwargs:
            if hasattr(worker,var):
                setattr(worker,var,kwargs[var])
        worker.fit(self.split_data['Train']['x'],self.split_data['Train']['y'])
        return worker.best_estimator_
        
    def accuracy(self):
        """ Calculate the Accuracy of the Regression Model """
        predict=self.model.predict(self.split_data['Test']['x'])
        errs=abs(predict-self.split_data['Test']['y'])
        MAE_P=100*np.mean(errs/self.split_data['Test']['y'])
        return 100- MAE_P

    def regression_report(self):
        """ Regression report collection """
        y_true,y_predic=self.split_data['Test']['y'],self.model.predict(self.split_data['Test']['x'])
        errors=y_true-y_predic
        percentiles=[5,25,50,75,95]
        perc_vals=np.percentile(errors,percentiles)

        reports=[
            ('Mean Absolute Error',metrics.mean_absolute_error(y_true,y_predic)),
            ('Mean Squared Error',metrics.mean_squared_error(y_true,y_predic)),
            ('Root Mean Squared Error',metrics.mean_squared_error(y_true,y_predic)),
            ('Mean Squared Log Error',metrics.mean_squared_log_error(y_true,y_predic)),
            ('Median Absolute Error',metrics.median_absolute_error(y_true,y_predic)),
            (' R{:} '.format('\xb2'),metrics.r2_score(y_true,y_predic)),
            (' Adjusted R{:} '.format('\xb2'),(1-(1-metrics.r2_score(y_true,y_predic))*(len(y_true)-1)/(len(y_true)-self.split_data['Test']['x'].shape[1]-1))),
            ('Mean Poisson Deviance',metrics.mean_poisson_deviance(y_true,y_predic)),
            ('Mean Gamma Deviance',metrics.mean_gamma_deviance(y_true,y_predic)),
            ('Max Error',metrics.max_error(y_true,y_predic)),
            ('Explained Variance',metrics.explained_variance_score(y_true,y_predic)),
            ('Mean Absolute Percentage Error',self.mean_absolute_percentage_error(y_true,y_predic))]

        print("".center(70,'_'))
        print(' Regression Metrics Report ')
        for metric,value in reports:
            print(f'{metric:>35s}: {value: >15.6f}')
        print("".center(70,'_'))
        print(' Percentiles ')
        for per,vals in zip(percentiles,perc_vals):
            print(f'{per:>15d}: {vals: >15.6f}')
    
    def mean_absolute_percentage_error(self,y_true,y_predic):
        """ Function emulates the function of the same name as is
        in sklearn.metrics of sklearn.__version__==0.24
        this is done for conda/anaconda related environment where sklearn.__version__==0.23.x 
        """
        errs=abs(y_predic-y_true)
        MAE_P=100*np.mean(errs/y_true)
        return MAE_P
    
    def residualTest(self,title,lineformat='C0:'):
        """ Plot Residual plot on Test Data"""
        Fig=plots.figure(figsize=(9,5.5));
        ax1=Fig.add_subplot(111);
        X=self.split_data["Test"]['x']
        X_lines=X.index
        YTrue=self.split_data["Test"]['y']
        YPred=self.model.predict(X)
        residualsPlot(X_lines,YTrue,YPred,title=title,linefmt=lineformat)
        plots.show()

def improvement(oldVAL,newVAL,title_text=''):
    """ Calculate improvement of a value over its old self 
     ******************
     Variables 
    -------------------
    oldVAL : old value of the variable 
    newVAL : new value of the variable 
    ____________________
    prints improvement percentage 
    returns improvement in percentage (float) """
    imprv=100*(newVAL-oldVAL)/oldVAL
    print(title_text)
    print(' Improved by {:0.3f}%'.format(imprv))
    return imprv