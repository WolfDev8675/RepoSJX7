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

resultOpDFrame=PD.read_csv(CS.uiGetFile())
CS.showTablehead(resultOpDFrame,"Result DataFrame")
#CS.showInformation("Result DataFrame Information ",FAS.FileAssessment(resultOpDFrame))

#GenCleaned=CLNS.cleanerPrimitive(generatorDFrame,{})
#ResCleaned=CLNS.cleanerPrimitive(resultOpDFrame,{})

gdc=CLNS.fixDebris(generatorDFrame,'Holding_Policy_Duration','14+','123')
CS.showTablehead(gdc,"** cleaned DataFrame")

mods=ITRS.Logistic()
mods.SplitRatio=(7.0/3)
mods.StudyData=generatorDFrame
mods.predictors=[]
mods.inferences=[Response]
mods.generateModel()
mods.generateMetrics()
mods.prediction(resultOpDFrame)