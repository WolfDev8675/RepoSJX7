#!usr/bin/python
 
#Code file: Cleaners.py
#Task: 
#**  Clean dataFrame depending on the type of
#**  operation chosen for the task. 
#**  Cleaning can be either the Convensional type 
#**  or the Imputation algorithm type

# imports 
import numpy as NP
import pandas as PD
import analytics as ALS
from sklearn.impute import KNNImputer as KNI



def find_Replace(dFrame=None,columnName=None,find=None,replace=None):
    """ Function find_Replace:
        Operation: find specific value from a particular column
        in a dataframe and replace the found value with the 
        replcement value 
        NB: this function is not effective against numpy.nan, numpy.NAN and numpy.NaN 
        since np.nan==np.nan is False which is same for other variants supplied by numpy
        as a result fails to find the respective data """
    positions=dFrame[dFrame[columnName]==find].index.tolist() # index list of changes
    for idx in positions: dFrame.loc[idx,columnName] = replace
  #end of function 


def removeNAN(dFrame=None):
    """ Function removeNAN:
        Operation: Remove NAN values or values in a pandas.DataFrame
        of the type of numpy.NAN(IEEE 754 floating point representation of Not a Number (NaN))
        via conventional methods viz., 
            1.	If the field of data is of categorical nature, then the missing records is to 
                field with the modal value of the non-empty data records.
            2.	If the field of data is of numerical continuous nature then we can either fill with Median or Mean,
                since Mean shifts more with data tendency shift than Median, Median is chosen to fill.
            """
    null_info= dict(dFrame.isnull().sum())
    nullcols=[]
    for cols in null_info: 
        if null_info[cols] > 0:nullcols.append(cols)
    for a_col in nullcols:
        if type(dFrame[a_col].dtype) is PD.CategoricalDtype:
            positions=dFrame[dFrame[a_col].isnull()].index.tolist() # index list of changes
            for idx in positions: dFrame.loc[idx,a_col] = dFrame[a_col].mode().tolist()[0] #mode fill
        elif type(dFrame[infos].dtype) is NP.dtype:
            positions=dFrame[dFrame[a_col].isnull()].index.tolist() # index list of changes
            for idx in positions: dFrame.loc[idx,a_col] = dFrame[a_col].median() #median fill
        else: pass   # no NULLs or NANs or NONEs ... code not supposed to execute (exclusive case)
  #end of function 
        

def imputeKNN(dFrame=None):
    """ Function imputeKNNN: 
        Operation: Using K-Nearest Neighbour algorithm to impute and fill 
        the empty places or data locations that is missing (viz., holds a numpy.NaN constant) 
        Function returns back data in encoded manner viz, coded functionality for categorized 
        values is not reverted back, this is also kept in this way keeping in mind that any other
        learner algorithms irrespective of nature recognizes the numerical encoded values than 
        string encoded numpy.object values """

    null_info= dict(dFrame.isnull().sum()) # information on the nulls 
    # Generating the Imputer Logic Object
    knnIR=KNI(n_neighbors=5,weights='uniform',metric='nan_euclidean')
    nan_cols=[]   # empty list to collect NANs or NULLs containing column names
    for cols in null_info:
        if(null_info[cols]):
            nan_cols.append(cols)  # appending column names
    nonIntNULLS=[]
    for cols in nan_cols:
        if(ALS.numericStrength(dFrame[cols])<50 and ALS.variety(dFrame[cols],95)[2]=='categorized'): nonIntNULLS.append(cols) # only categorised can be in this error section
        elif(ALS.numericStrength(dFrame[cols])>50):pass
        else: nan_cols.remove(cols)    # supposed to be object(string miscellaneous) type hence not to be considered 

    mapsOfChanges=dict.fromkeys(nonIntNULLS,{}) 
    for a_col in nonIntNULLS:
        #Quintuple-Step Process
        #1: Pre Conversion Tag Listing
        pr_ctl=ALS.variety(dFrame[a_col],95)[0]
        #2: Conversion
        dFrame[a_col]=dFrame[a_col].cat.codes  
        dFrame=ALS.reset_columnData(dFrame,{a_col:'category'})
        #3: Post Conversion Tag Listing
        po_ctl=ALS.variety(dFrame[a_col],95)[0]
        #4: Map index by population to Change register
        for key in po_ctl: 
            contents=list(pr_ctl.items())
            for i in range(len(contents)):
                if(po_ctl[key]==contents[i][1]):
                    mapsOfChanges[a_col][key]=contents[i][0]
        #5: Return Nulls
        ret_idxs=dFrame[dFrame[a_col] == -1 ].index.tolist() #since catgorical coding changed NULLS to (-1) 
        for idx in ret_idxs: dFrame.loc[idx,a_col]= NP.nan

    knnIR.fit(dFrame[nan_cols])  #fitting
    dFrame[nan_cols]=knnIR.transform(dFrame[nan_cols]) # finalising imputation task
    
    #Return Changes
    return dFrame
  #end of function   
