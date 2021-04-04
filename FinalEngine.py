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

# Start of Code 

generatorDFrame=PD.read_csv(CS.uiGetFile())
CS.showTablehead(generatorDFrame,"Primary DataFrame")
CS.showInformation("Primary DataFrame Information ",FAS.FileAssessment(generatorDFrame))

resultOpDFrame=PD.read_csv(CS.uiGetFile())
CS.showTablehead(resultOpDFrame,"Result DataFrame")
CS.showInformation("Result DataFrame Information ",FAS.FileAssessment(resultOpDFrame))

CLNS.cleanerPrimitive(generatorDFrame,{})
