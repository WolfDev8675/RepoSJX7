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

#boxplot
#plots.boxplot(dHs[['Open','High','Low','Close']],labels=['Open','High','Low','Close']);plots.show()

#1: Linear Regression
#frCst1=Forecaster(model=LinReg())
#frCst1.pushData(data=dHs,predicts=['Open','High','Low'],infers="Close")
#frCst1.normal_split()
#frCst1.train()
#anotStr1='\n'.join((r"Mean Absolute Error: %f"%metrics.mean_absolute_error(frCst1.YData,frCst1.model.predict(frCst1.XData)),
#r" Mean Squared Error:  %f"%metrics.mean_squared_error(frCst1.YData,frCst1.model.predict(frCst1.XData)),
#r" Root Mean Squared Error:  %f"%np.sqrt(metrics.mean_squared_error(frCst1.YData,frCst1.model.predict(frCst1.XData)))))
#predLR=frCst1.model.predict(dhs2[['Open','High','Low']])
#Fig1=plots.figure(figsize=(15,7.5));ax1=Fig1.add_subplot(111);#Fig1.canvas.manager.full_screen_toggle()
#plots.plot(dhs2.index,dhs2[['Close']])
#plots.plot_date(dhs2.index,predLR,'g.-')
#plots.text(0.12,0.95,anotStr1,horizontalalignment='center',
#     verticalalignment='center', transform=ax1.transAxes)
#plots.title("model: Linear Regression ")
#plots.show()
#frCst1.plotMetrics(data=dhs2,title='Model: Linear Regression ')

#frCst2=Forecaster(model=LinReg())
#frCst2.pushData(data=dHs,predicts=['Open','High','Low'],infers="Close")
#frCst2.crossval_KF_split(n_splits=5,random_state=None,shuffle=False)
#frCst2.train()
#frCst2.plotMetrics(data=dhs2,title='Model: Linear Regression ')

#print("\n\n Linear Regression metrics ")
#print(" Mean Absolute Error %f"%metrics.mean_absolute_error(frCst1.YData,frCst1.model.predict(frCst1.XData)))
#print(" Mean Squared Error  %f"%metrics.mean_squared_error(frCst1.YData,frCst1.model.predict(frCst1.XData)))
#print(" Root Mean Squared Error  %f"%np.sqrt(metrics.mean_squared_error(frCst1.YData,frCst1.model.predict(frCst1.XData))))

##2: Random Forest 
#frCst2=Forecaster(model=RnForReg())
#frCst2.pushData(data=dHs,predicts=['Open','High','Low'],infers="Close")
#frCst2.train()
#predRFR=frCst2.model.predict(dhs2[['Open','High','Low']])
#plots.figure()
#plots.plot(dhs2.index,dhs2[['Close']])
#plots.plot_date(dhs2.index,predRFR,'g.-')
#plots.title("model: Random Forest Regression ")
#plots.show()
#print("\n\n Random Forest metrics ")
#print(" Mean Absolute Error %f"%metrics.mean_absolute_error(frCst2.YData,frCst2.model.predict(frCst2.XData)))
#print(" Mean Squared Error  %f"%metrics.mean_squared_error(frCst2.YData,frCst2.model.predict(frCst2.XData)))
#print(" Root Mean Squared Error  %f"%np.sqrt(metrics.mean_squared_error(frCst2.YData,frCst2.model.predict(frCst2.XData))))

##3: Support Vector  
#frCst3=Forecaster(model=SVR())
#frCst3.pushData(data=dHs,predicts=['Open','High','Low'],infers="Close")
#frCst3.train()
#predSVR=frCst3.model.predict(dhs2[['Open','High','Low']])
#plots.figure()
#plots.plot(dhs2.index,dhs2[['Close']])
#plots.plot_date(dhs2.index,predSVR,'g.-')
#plots.title("model: Support Vector Regression ")
#plots.show()
#print("\n\n Support Vector metrics ")
#print(" Mean Absolute Error %f"%metrics.mean_absolute_error(frCst3.YData,frCst3.model.predict(frCst3.XData)))
#print(" Mean Squared Error  %f"%metrics.mean_squared_error(frCst3.YData,frCst3.model.predict(frCst3.XData)))
#print(" Root Mean Squared Error  %f"%np.sqrt(metrics.mean_squared_error(frCst3.YData,frCst3.model.predict(frCst3.XData))))

##4: Bayesian Ridge  
#frCst4=Forecaster(model=BayesR())
#frCst4.pushData(data=dHs,predicts=['Open','High','Low'],infers="Close")
#frCst4.train()
#predNvByR=frCst4.model.predict(dhs2[['Open','High','Low']])
#plots.figure()
#plots.plot(dhs2.index,dhs2[['Close']])
#plots.plot_date(dhs2.index,predNvByR,'g.-')
#plots.title("model: Bayesian Ridge Regression ")
#plots.show()
#print("\n\n Baysean Ridge metrics ")
#print(" Mean Absolute Error %f"%metrics.mean_absolute_error(frCst4.YData,frCst4.model.predict(frCst4.XData)))
#print(" Mean Squared Error  %f"%metrics.mean_squared_error(frCst4.YData,frCst4.model.predict(frCst4.XData)))
#print(" Root Mean Squared Error  %f"%np.sqrt(metrics.mean_squared_error(frCst4.YData,frCst4.model.predict(frCst4.XData))))


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
for mod_key in models_mods_norm:
    models_mods_norm[mod_key].pushData(data=dHs,predicts=['Open','High','Low'],infers="Close")
    models_mods_norm[mod_key].normal_split()
    models_mods_norm[mod_key].train()
    models_mods_norm[mod_key].plotMetrics(data=dhs2,title="Model: "+models_name[mod_key])

for mod_key in models_mods_CVKF:
    models_mods_CVKF[mod_key].pushData(data=dHs,predicts=['Open','High','Low'],infers="Close")
    models_mods_CVKF[mod_key].crossval_KF_split(n_splits=5,random_state=None,shuffle=False)
    models_mods_CVKF[mod_key].train()
    models_mods_CVKF[mod_key].plotMetrics(data=dhs2,title="Model: "+models_name[mod_key]+" Cross Validated ")