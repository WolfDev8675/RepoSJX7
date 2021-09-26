#!usr/bin/python

""" RUNTIME Backend Executable for the operation """
# Target job: predict Brent blend Crude oil prices 

#imports 
from DataAccess import *
from Intelligence import * 
import matplotlib.pyplot as plots  #@visuals
from statsmodels.tsa.seasonal import seasonal_decompose  #@pre-analysis
from sklearn.model_selection import train_test_split  #@intelligence
from sklearn import metrics #@post-analysis
from sklearn.linear_model import LinearRegression as LinReg  #@intellligence
from sklearn.ensemble import RandomForestRegressor as RnForReg  #@intelligence
from sklearn.svm import SVR #@intelligence
from sklearn.linear_model import BayesianRidge as BayesR   #@intelligence
from copy import deepcopy


# historic data access
# dHs=data_Prestored("https://raw.githubusercontent.com/WolfDev8675/RepoSJX7/CaseStudy_backend/Data_static/BrentOilPrices.csv")

dHs=data_FixedTimeLine("BZ=F",start="2017-10-01",end="2019-10-01")  #for prediction
dhs2=data_Live(period='5mo')                                        #for result comparison    
# Season 
model_TS=seasonal_decompose(dHs[['Close']],model='additive',period=30)
model_TS.plot()
plots.show() 

#boxplot @visuals 
plots.boxplot(dHs[['Open','High','Low','Close']],labels=['Open','High','Low','Close']);plots.show()
 
# EDA 
# yearwise trend open vs close and high alternations check @visuals
#import seaborn 
#seaborn.pairplot(dHs[['Open','High','Low','Close']]);plots.show()
## per year open and close line curves 


# 

#Model Creation and study
models_name={'LR':"Linear Regression",
             'RF':"Random Forest",
             'SV':"Support Vector",
             'BR':"Bayesian Ridge"};
models_mods_norm={'LR':Forecaster(model=LinReg()),
                  'RF':Forecaster(model=RnForReg()),
                  'SV':Forecaster(model=SVR()),
                  'BR':Forecaster(model=BayesR())};
models_mods_CVKF=deepcopy(models_mods_norm);

# Train and Test 
#for mod_key in models_mods_norm:
#    models_mods_norm[mod_key].pushData(data=dHs,predicts=['Open','High','Low'],infers="Close")
#    models_mods_norm[mod_key].normal_split()
#    models_mods_norm[mod_key].train()
#    models_mods_norm[mod_key].plotMetrics(data=dhs2,title="Model: "+models_name[mod_key])

for mod_key in models_mods_CVKF:
    models_mods_CVKF[mod_key].pushData(data=dHs,predicts=['Open','High','Low'],infers="Close")
    models_mods_CVKF[mod_key].crossval_KF_split(n_splits=5,random_state=None,shuffle=False)
    models_mods_CVKF[mod_key].train()
    models_mods_CVKF[mod_key].plotMetrics(data=dhs2,title="Model: "+models_name[mod_key]+" Cross Validated ")

#Report on models 
for mod_key in models_mods_CVKF:
    if mod_key is not 'LR':
        print(models_name[mod_key])
        models_mods_CVKF[mod_key].regression_report()
    else:
        print(models_name[mod_key])
        models_mods_CVKF[mod_key].grad_decent()
        models_mods_CVKF[mod_key].ensemble_grading()
        models_mods_CVKF[mod_key].boost()
        models_mods_CVKF[mod_key].regression_report()

# Report on train vs test vs predicted
#  predicted vs test plot report  @visuals 
#  kind of residuals plots  
# Reasons and conclusions + post decisions and future advs 