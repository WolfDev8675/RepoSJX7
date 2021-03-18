#!usr/bin/python

# Question 
# ... Read car data.csv and car condition.csv. Merge them together (files already provided). 
#       Find out following from the data set.
#   1. Group data by origin
#   2. Group data by car condition.
#..

# Start of codes
#.. 

#imports
import pandas as PD
import numpy as NP
import analytics as ALS


# data file access
rootpath=input("Please input the Path containing the Data ")
if rootpath=="" : rootpath="data\\"
file1name="car data.csv"
file2name="car condition.csv"
try:
    # Question 
    with open(rootpath+"qscx.txt") as qsc:
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

# Task Sessions 
#1: Group data by origin
print(" TASK 1: Group data by origin .... ")
Gr_Org=c_mer_moded.groupby(['origin'],axis=0)
    # printing details 
for key,value in Gr_Org:
    print(key," :: \n", Gr_Org.get_group(key), " \n ")  #Using exclusive method by exploiting each groups limits by loops


#2: Group data by car condition.
print(" TASK 2: Group data by car condition .... ")
Gr_Cond=c_mer_moded.groupby(['Condition'],axis=0)
print(Gr_Cond.apply(print))      # Using inclusive/native method of GroupBy object  

# end of code .....
