#!usr/bin/python

# Code file: FinalEngine.py
# Task: 
##Final code to execute all processes sequentially in a manner as 
##required to complete the task  properly

# imports
import pandas as PD
import analytics as ALS
import Cosmetics as CS
import DataManager as FAS
import Cleaners as CLNS
import Interpretors as ITRS
import random as RDS
from time import process_time as PRT

# Start of Code 

## Acquire Data and print primary details + show data 
print(" Acquiring Data ..... ",);cT=PRT()
#1
GenDFrame=PD.read_csv(CS.uiGetFile())
CS.showTable(GenDFrame,"Primary DataFrame")
CS.showInformation("Primary DataFrame Information ",FAS.dataInfo(GenDFrame)+'\n'+GenDFrame.describe().to_string());
#2
ResDFrame=PD.read_csv(CS.uiGetFile())
CS.showTable(ResDFrame,"Result DataFrame")
CS.showInformation("Result DataFrame Information ",FAS.dataInfo(ResDFrame)+'\n'+ResDFrame.describe().to_string());
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

## Remove irregularities ( 14+ in 'Holding_Policy_Duration' field)
print(" Oddities Clean .... ",)
CLNS.find_Replace(GenDFrame,'Holding_Policy_Duration','14+',RDS.randint(15,20))   #1
CLNS.find_Replace(ResDFrame,'Holding_Policy_Duration','14+',RDS.randint(15,20))   #2
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

## Fix datatypes of fields
print(" Datatype Fixing .... ",)
GenDFrame=FAS.FixDataByPopulation(GenDFrame)    #1
ResDFrame=FAS.FixDataByPopulation(ResDFrame)    #2
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

## Fixing Specific field datatype shift *** field: Holding_Policy_Duration due to less variations gets categorized 
print(" Fixing Specific field datatype shift ... ")
GenDFrame=ALS.reset_columnData(GenDFrame,{'Holding_Policy_Duration':'numerical'})
ResDFrame=ALS.reset_columnData(ResDFrame,{'Holding_Policy_Duration':'numerical'})
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

### Scaling Data 
#print(" Scaling operation... ")
##scalables=CS.selectFromLists(" Scalable fields "," Select labels to scale ",GenDFrame.columns.to_list())[0]
#GenDFrame=FAS.scaleData(GenDFrame)
#ResDFrame=FAS.scaleData(ResDFrame)
#print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

## Remove NAN values  ** Comment/Uncomment required section 
print(" NaN Clean .... ",) 
#print(" Conventional Median/Mode filler method ...... ",)
#GenDFrame=CLNS.removeNAN(GenDFrame)     #1
#ResDFrame=CLNS.removeNAN(ResDFrame)     #2 
print(" K Nearest Neighbour Imputation method ...... ",)
GenDFrame=CLNS.imputeKNN(GenDFrame)     #1
ResDFrame=CLNS.imputeKNN(ResDFrame)     #2
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

## Reprint details : post cleaning
print("Post Clean Data Review... ")
CS.showInformation("Primary DataFrame Information ",FAS.dataInfo(GenDFrame)+'\n'+GenDFrame.describe().to_string())      #1
CS.showInformation("Result DataFrame Information ",FAS.dataInfo(ResDFrame)+'\n'+ResDFrame.describe().to_string())       #2
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

## Setting the column names 
print(" Parameter Set .... ",)
#predict=['City_Code','Region_Code','Accomodation_Type','Reco_Insurance_Type',
#                 'Upper_Age','Lower_Age','Is_Spouse','Health Indicator','Holding_Policy_Duration',
#                 'Holding_Policy_Type','Reco_Policy_Cat','Reco_Policy_Premium']
#infer=['Response']
plotLab=CS.selectFromLists(" Plot labels "," Select labels to plot ",GenDFrame.columns.to_list())[0]
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

## Plots of fields ** histogram or boxplot depending on failure criteria
print(" Generating Plots.... ")
FAS.showPlots(GenDFrame,plotLab,'Plots: Primary Data')
FAS.showPlots(ResDFrame,plotLab,'Plots: Secondary Data')
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

## Encode enforcement Categorical number coding 
#print(" Fixing Categorical fields not handled while NAN Removal ..... ")
#FAS.encodeImpose(GenDFrame,predict)     #1
#FAS.encodeImpose(ResDFrame,predict)     #2
print(" Fixing Categorical fields not handled while NAN Removal ..... pushing Dummies ")
GenDFrame=FAS.encodeDummy(GenDFrame,GenDFrame.columns.to_list())     #1
ResDFrame=FAS.encodeDummy(ResDFrame,ResDFrame.columns.to_list())     #2
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

CS.showInformation("Primary DataFrame Information ",FAS.dataInfo(GenDFrame)+'\n'+GenDFrame.describe().to_string())      #1
CS.showInformation("Result DataFrame Information ",FAS.dataInfo(ResDFrame)+'\n'+ResDFrame.describe().to_string())       #2
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()


## Select predictors and infers for LogisticRegression
[predict,infer]=CS.selectFromLists(" Predictables and Inferences  "," Select predictables  ",GenDFrame.columns.to_list()," Select inferences  ",GenDFrame.columns.to_list())
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

## Initiate Logistic Model
print(" Initiating Logistic Model ... ",)
mods=ITRS.Logistic(solver='lbfgs',max_iter=100000)
mods.SplitRatio=(7.0/3)
mods.pushData(GenDFrame,predict,infer)
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

## Train Logistic model
print(" Training Model ... ",)
mods.generateModel()
mods.generateMetricsPlots()
CS.showInformation(" Model Metrics ",mods.generateMetricsInfo())
print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()

## Retrain options
retrain=True;attempt=0
print(" Retrain Model... ")
while(retrain):
    retrain=CS.decisionMessage(" Retrain Options "," Retrain Model ? ....")
    if retrain:
        mods.retrainModel()
        CS.showInformation(" Model Metrics ",mods.generateMetricsInfo())
        attempt+=1
        print(" Attempt = ",attempt)
    print(" Success. ... Process time (s) ",(PRT()-cT));cT=PRT()
print(" Retrain attempts = ",attempt)

## Applying Trained Model to Unknown data
print(" Applying Model to Unknown Data ")
results=mods.predictionApply(ResDFrame[mods.predictors]) #numpy.ndarray
CS.showTable(FAS.matchResponse(ResDFrame,results,'Response'),"Required Result")
print(" Success. ... Process time (s) ",(PRT()-cT))

#... End of codes
# END OF FILE: 'FinalEngine.py'