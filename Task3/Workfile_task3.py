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
rootpath=input("Please input the Path containg the Data ")
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

# creating copy 
dbx1=CP.deepcopy(c_mer_moded) 
# operations
for infos in null_info:
    # NB. null_info contains info of columns where there is no null 
    if null_info[infos] < 3 and null_info[infos] !=0 :
        # number of NULLs is less than three but has NULL is confirmed 
        del_list=dbx1[dbx1[infos].isnull].index.toList()  # indices for removal of rows
        dbx1.drop(axis=0,index=del_list,inplace=True) # removing records
    elif null_info[infos] != 0:
        # all other NULL hits 
        if type(dbx1[infos].dtype) is PD.CategoricalDType:
            exchange_null=dbx1[infos].mode().tolist()[0] # question 4 directive 
        elif type(dbx1[infos].dtype) is NP.dtype:
            exchange_null=dbx1[infos].median()  # question 3 directive
        else: pass   # no NULLs or NANs or NONEs ... code not supposed to execute
        
