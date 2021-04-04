#!usr/bin/python
 
#Code file: Cleaners.py
#Task: 
#**  Clean dataFrame depending on the type of
#**  operation chosen for the task. 
#**  Cleaning can be either the Convensional type 
#**  or the Imputation algorithm type

# imports 
import pandas as PD
import analytics as ALS

def cleanerPrimitive(dFrame,columnDetail):
    """ function """
    pass

def fixDebris(dFrame,column,find,replace):
    """ function """
    dCopy=dFrame
    dCopy[column==find]=replace
    return dCopy