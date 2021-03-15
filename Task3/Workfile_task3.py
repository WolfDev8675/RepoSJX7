#!usr/bin/python
#
# Question:  Code to operate on two data files provided 
# files kept localy at path: data\\ 
# Read car data.csv and car condition.csv. Merge them together (files already provided). Find out following from the data set.
#1. How many null values were there in the dataset for each column?
#2. If number of null values are less than 3, delete rows containing null values.
#3. Else, fill null values of numerical columns with mean/median.
#4. Fill categorical columns with mode.
#5. Apply KNN Imputation technique to fill up null values.
#** 

# Start of codes
#.. 

#imports
import pandas as PD
import numpy as NP
import analytics as ALS
import copy as CP
from sklearn.impute import KNNImputer as KNI

# data file access
rootpath=input("Please input the Path containing the Data ")
if rootpath=="" : rootpath="data\\"
file1name="car data.csv"
file2name="car condition.csv"
try:
    # Question 
    with open(rootpath+"qsc.txt") as qsc:
        print(qsc.read())
except:
    print(" Question not found ")
    
# Alignment marker 
print("\n\n")

try:
    # Dataframes 
    cdcsv=PD.read_csv(rootpath+file1name)  # car data
    cccsv=PD.read_csv(rootpath+file2name)  # car condition
    print("Car data \n",cdcsv); print("Car condition \n",cccsv) 
    # previous knowledge of datasets: both have 'car id' column 
    c_mer=cdcsv.merge(cccsv,left_on='car id',right_on='car id')
    print(c_mer)
except:
    print(" Fatal Error : Datasets not found    ......       Closing code ")
    raise SystemExit

#.. 
typer0={}  # empty dictionaries for recognising data nature 
typer1={}
#establishing character of dataset
for col in c_mer.columns:
    typer0[col]=[ALS.variety(c_mer[col],95)[2],ALS.numericStrength(c_mer[col])]
# establishing fulfilment criteria of dataset 
for element in typer0:
    if typer0[element][0].startswith('random'):  
        if typer0[element][1]>50: typer1[element]='numerical'
        else: typer1[element]='object'
    elif typer0[element][0].startswith('categ'): 
        typer1[element]='category'

# finalizing changes 
c_mer_moded=ALS.reset_columnData(c_mer,typer1)

#..
# Question 1: How many null values were there in the dataset for each column
#       generating informations of null values in the data
null_info= dict(c_mer_moded.isnull().sum()) 
print(" Question 1: How many null values were there in the dataset for each column :  \n",'columns'.center(20,' '),' NULLs ')# print 
for infos in null_info:
    print(infos.center(20," "),"  ",null_info[infos])

# Alignment marker 
print("\n\n")
#..
#Questions 2,3,4:
# * If number of null values are less than 3, delete rows containing null values.
# * Else, fill null values of numerical columns with mean/median. (taking median)
# * Fill categorical columns with mode.
qtx=""" #Questions 2,3,4:
 * If number of null values are less than 3, delete rows containing null values.
 * Else, fill null values of numerical columns with mean/median. (taking median)
 * Fill categorical columns with mode. """
print(qtx)
# creating copy 
dbx1=CP.deepcopy(c_mer_moded) 
# operations
for infos in null_info:
    # NB. null_info contains info of columns where there is no null 
    if null_info[infos] < 3 and null_info[infos] !=0 :
        # number of NULLs is less than three but has NULL is confirmed 
        del_list=dbx1[dbx1[infos].isnull()].index.tolist()  # indices for removal of rows
        dbx1.drop(axis=0,index=del_list,inplace=True) # removing records
    elif null_info[infos] != 0:
        # all other NULL hits
        hit=0
        if type(dbx1[infos].dtype) is PD.CategoricalDtype:
            exchange_null=dbx1[infos].mode().tolist()[0] # question 4 directive
            hit=1
        elif type(dbx1[infos].dtype) is NP.dtype:
            exchange_null=dbx1[infos].median()  # question 3 directive
            hit=1
        else: pass   # no NULLs or NANs or NONEs ... code not supposed to execute (exclusive case)
        if (hit):
            change_list=dbx1[dbx1[infos].isnull()].index.tolist() # index list of changes
            for idx in change_list: dbx1.loc[idx,infos]= exchange_null # registering changes
    else: pass     # no NULLs or NANs or NONEs ... code not supposed to execute (exclusive case) 
# end of for loop
#..
# printing proof 
print("\n Edited Data ")
print(dbx1.info())
print("NULL information \n")
print(dbx1.isnull().sum())
print("\n Original data ")
print(c_mer_moded.info())
print("NULL information \n")
print(c_mer_moded.isnull().sum())
#..
# Alignment marker 
print("\n\n")

#..
# Question 5:  Apply KNN Imputation technique to fill up null values.
print(" Question 5:  Apply KNN Imputation technique to fill up null values.")
dbx2=CP.deepcopy(c_mer_moded) # Secondary copy for KNN task (Question 5)
# Generating the Imputer Logic Object
knnIR=KNI(n_neighbors=5,weights='uniform',metric='nan_euclidean')
nan_cols=[]   # empty list to collect NANs or NULLs containing column names
for cols in null_info:
    if(null_info[cols]):
        nan_cols.append(cols)  # appending column names
nonIntNULLS=[]
for cols in nan_cols:
    if(ALS.numericStrength(dbx2[cols])<50 and ALS.variety(dbx2[cols],95)[2]=='categorized'): nonIntNULLS.append(cols) # only categorised can be in this error section
    elif(ALS.numericStrength(dbx2[cols])>50):pass
    else: nan_cols.remove(cols)    # supposed to be object(string miscellaneous) type hence not to be considered 

mapsOfChanges=dict.fromkeys(nonIntNULLS,{}) 
for a_col in nonIntNULLS:
    #Quintuple-Step Process
    #1: Pre Conversion Tag Listing
    pr_ctl=ALS.variety(dbx2[a_col],95)[0]
    #2: Conversion
    dbx2[a_col]=dbx2[a_col].cat.codes  
    dbx2=ALS.reset_columnData(dbx2,{a_col:'category'})
    #3: Post Conversion Tag Listing
    po_ctl=ALS.variety(dbx2[a_col],95)[0]
    #4: Map index by population to Change register
    for key in po_ctl: 
        contents=list(pr_ctl.items())
        for i in range(len(contents)):
            if(po_ctl[key]==contents[i][1]):
                mapsOfChanges[a_col][key]=contents[i][0]
    #5: Return Nulls
    ret_idxs=dbx2[dbx2[a_col] == -1 ].index.tolist() #since catgorical coding changed NULLS to (-1) 
    for idx in ret_idxs: dbx2.loc[idx,a_col]= NP.nan

knnIR.fit(dbx2[nan_cols])  #fitting
dbx2[nan_cols]=knnIR.transform(dbx2[nan_cols]) # finalising imputation task
# end of inputer section KNN
#..

# Returning Mapping (Only for Categorical values)
for keys in mapsOfChanges:
    dbx2[keys]=round(dbx2[keys]) # correcting non categorized Decimals 
    dbx2[keys].map(mapsOfChanges[keys])
    dbx2=ALS.reset_columnData(dbx2,{keys:'category'})

# printing proof 
print("\n Edited Data (KNN Imputer)")
print(dbx2.info())
print("NULL information \n")
print(dbx2.isnull().sum())
print("\n Original data ")
print(c_mer_moded.info())
print("NULL information \n")
print(c_mer_moded.isnull().sum())
#..

##end of codes
#.. 
