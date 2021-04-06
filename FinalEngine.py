#!usr/bin/python

# Code file: FinalEngine.py
# Task: 
##Final code to execute all processes sequentially in a manner as 
##required to complete the task  properly

# imports
import pandas as PD
import Cosmetics as CS
import FileAssessment as FAS
import Cleaners as CLNS
import Interpretors as ITRS
import random as RDS

# Start of Code 

generatorDFrame=PD.read_csv(CS.uiGetFile())
CS.showTablehead(generatorDFrame,"Primary DataFrame")
#CS.showInformation("Primary DataFrame Information ",FAS.FileAssessment(generatorDFrame))
#$$
#resultOpDFrame=PD.read_csv(CS.uiGetFile())
#CS.showTablehead(resultOpDFrame,"Result DataFrame")
#CS.showInformation("Result DataFrame Information ",FAS.FileAssessment(resultOpDFrame))

#GenCleaned=CLNS.cleanerPrimitive(generatorDFrame,{})
#ResCleaned=CLNS.cleanerPrimitive(resultOpDFrame,{})

#gdc=CLNS.fixDebris(generatorDFrame,'Holding_Policy_Duration','14+','123')
#CS.showTablehead(gdc,"** cleaned DataFrame")


mods=ITRS.Logistic(solver='lbfgs',max_iter=100000)
mods.SplitRatio=(7.0/3)
mods.StudyData=generatorDFrame
#mods.predictors=['City_Code','Region_Code','Accomodation_Type','Reco_Insurance_Type',
#                 'Upper_Age','Lower_Age','Is_Spouse','Health Indicator','Holding_Policy_Duration',
#                 'Holding_Policy_Type','Reco_Policy_Cat','Reco_Policy_Premium']
#mods.inferences=[Response]
mods.predictors=['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
mods.inferences=['Outcome']
mods.generateModel()
mods.generateMetrics()
#results=mods.prediction(resultOpDFrame)
print(mods.confMatrix)
