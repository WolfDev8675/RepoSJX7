#!usr/bin/python

# Question .....
# Read car data.csv and car condition.csv. Merge them together
#   (files already provided). And complete following tasks.
#   1. Plot bar chart, box-plot, violin plot, line plot.
#   2. Build correlation matrix.
#   3. Show distribution of data.
#   4. Describe different statistics of data
#..

# Start of code 
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


#   1. Plot bar chart, box-plot, violin plot, line plot.
#   2. Build correlation matrix.
#   3. Show distribution of data.


#   4. Describe different statistics of data
print(" 4. Describe different statistics of data ")
print(c_mer_moded.describe())