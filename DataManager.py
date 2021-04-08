#!usr/bin/python
 
#Code file: DataManager.py
#Task: 
#**  information and assimilation of the 
#**  data content of a pandas.DataFrame object 

#imports 
import pandas as PD
import io
import analytics as ALS

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