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

def fixDebris(dFrame,columnDetail):
    """ function """
    pass

<<<<<<<< HEAD:Cleaners.py
def fixDebris(dFrame,column,find,replace):
    """ function """
    dCopy=dFrame
    dCopy[column==find]=replace
    return dCopy
========
>>>>>>>> ce89e68fdb754841e2ab12d35071834feab815af:CLeaners.py
