#!usr/bin/python
 
#Code file: DataManager.py
#Task: 
#**  information and assimilation of the 
#**  data content of a pandas.DataFrame object 

#imports 
import pandas as PD
import numpy as NP
import io
import analytics as ALS
import matplotlib.pyplot as PLOT
from sklearn.preprocessing import *

def FixDataByPopulation(dFrame):
    """ Function FixDataByPopulation:
        Operation: assess the population strength and identify
         if a certain field is categorizable or not and depending on that 
         try to fix the pandas.DataFrame object to specific datatypes respective of fields """

    typer0={}  # empty dictionaries for recognising data nature 
    typer1={}
    #establishing character of dataset
    for col in dFrame.columns:
        typer0[col]=[ALS.variety(dFrame[col],95)[2],ALS.numericStrength(dFrame[col])]
    # establishing fulfilment criteria of dataset 
    for element in typer0:
        if typer0[element][0].startswith('random'):  
            if typer0[element][1]>50: typer1[element]='numerical'
            else: typer1[element]='object'
        elif typer0[element][0].startswith('categ'): 
            typer1[element]='category'

    return ALS.reset_columnData(dFrame,typer1)
  #end of function 

def matchResponse(dFrame,response,responseName):
    """Function  matchResponse 
       Operation: match a response input to the 
       corresponding dataframe using the key or 
       hashable column of the dataframe """
    dFrameResp=PD.Series(response)
    keyName=ALS.detectKeys(dFrame)[0]
    if keyName is 'index': dFrameKey=dFrame.index
    else: dFrameKey=dFrame[keyName]
    return PD.DataFrame({keyName:dFrameKey,responseName:dFrameResp})
 #end of function  

def dataInfo(dFrame):
    """ Function dataInfo:
        Operation:  push the results of pandas.DataFrame.info from 
        the sys.stdout buffer to a local string buffer to be used as a string function """
    buffer=io.StringIO()
    dFrame.info(buf=buffer)
    return buffer.getvalue()
  #end of function 

def showPlots(dFrame=None,fieldNames=None,winTitle='Plot Figure'):
    """ Function  showPlots:
        Operation: plot Boxplots or Histograms of the data fields 
         Histograms are plotted for Categorical fields, while,
         Boxplots are plotted for Numerical fields"""

    fieldNames_refined=fieldNames
    for field in fieldNames: 
        if dFrame[field].dtype == NP.object : fieldNames_refined.remove(field)
    nosFields=len(fieldNames_refined)
    TmpNF=(nosFields-1) if (nosFields%3 and nosFields%4 and nosFields%5) else nosFields
    axC=5 if not TmpNF%5 else 4 if not TmpNF%4 else 3 if not TmpNF%3 else None
    axR=int(TmpNF/axC); axR= axR if TmpNF is nosFields else axR+1 
    pos=1
    PLOT.figure(figsize=(13,7.5)).canvas.set_window_title(winTitle)
    for col in fieldNames:
        PLOT.subplot(axR,axC,pos)
        if dFrame[col].dtype == NP.int64 or dFrame[col].dtype == NP.float64:
            dFrame.boxplot(column=col)
        elif type(dFrame[col].dtype) == PD.CategoricalDtype:
            dFrame[col].hist()
        else: pass # non executable section 
        pos+=1
    PLOT.show()
  #end of function 

def encodeImpose(dFrame=None,fieldNames=None):
    """ Function encodeImpose:
        Operation: Encode categorical datatypes to number coded categories """
    for field in fieldNames:
        if type(dFrame[field].dtype) == PD.CategoricalDtype:
            dFrame[field]=PD.Categorical(values=dFrame[field].cat.codes)
        else: pass
    return dFrame
  #end of function

def encodeDummy(dFrame=None,fieldNames=None):
    """ Function encodeDummy:
        Operation: Encode Categorical datatypes to dummy variables
        and add them to dataframe """
    RetFrame=dFrame
    EncodedCols=[]
    DumbColumns=[]
    for field in fieldNames:
        if type(dFrame[field].dtype) == PD.CategoricalDtype:
            oneDumbColumn=PD.get_dummies(dFrame[field])
            EncodedCols.append(field)
            #./ Fixing Dummies to Original
            DumbColumns.extend(oneDumbColumn.columns.to_list())
            RetFrame=PD.concat([RetFrame,oneDumbColumn],axis=1)
    return [RetFrame,EncodedCols,DumbColumns]
   #end of function

  
def scaleData(dFrame=None):
    """ Function scaleData:
        Operation: Use a standard scaler on the numerical fields of data
        and thereby standardise the data given 
    """ 
    scaler=StandardScaler()
    allCols=dFrame.columns.to_list();modified=dFrame
    numerics=[]; [numerics.append(col) for col in allCols if (dFrame[col].dtype == NP.int64 or dFrame[col].dtype == NP.float64)]
    scaled=PD.DataFrame(data=scaler.fit_transform(dFrame[numerics]),columns=numerics)
    modified[numerics]=scaled
    return modified



  #** end of code 
#END OF FILE 'DataManager.py' 