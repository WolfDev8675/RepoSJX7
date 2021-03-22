#!usr/bin/python

# Question ...... 
#  Read car data.csv and car condition.csv. Merge them together
#   (files already provided). Find out following from the data set.
#   1. Apply dummy encoding.
#   2. Do same functionality using one-hot encoding.
#   3. Apply level encoding
#..

# Start of code 
#..

#imports
import pandas as PD
import analytics as ALS
import copy as CP
from sklearn.preprocessing import OneHotEncoder as OHE

# data file access
rootpath=input("Please input the Path containing the Data ")
if rootpath=="" : rootpath="data\\"
file1name="car data.csv"
file2name="car condition.csv"
try:
    # Question 
    with open(rootpath+"qsxc.txt") as qsc:
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
PD.set_option('display.max_columns', None) # momentary set for session to show all columns
# primary setup completed 

#.**  Operations ** 
#./ Setting primaries
cat_columns=[]
for column in typer1:
    if(typer1[column] is 'category'): cat_columns.append(column)

# 1. Apply dummy encoding.
print(" 1. Operation by applying Dummy Encoding ")
#./ Individual Copy
data4OP1=CP.deepcopy(c_mer_moded)
#./ Getting Dummies
dummy=PD.get_dummies(data4OP1[cat_columns])
#./ Fixing Dummies to Original
finalOP1=PD.concat([data4OP1,dummy],axis=1)
#./ Printing  
print(finalOP1)

# 2. Do same functionality using one-hot encoding.
print(" 2. Operation by applying One-Hot Encoding ")
#./ Individual Copy
data4OP2=CP.deepcopy(c_mer_moded)
#./ Getting Encoder 
encoder=OHE(handle_unknown='error',drop ='first')#,categories=cat_columns)
encoded=encoder.fit_transform(data4OP2[cat_columns]).toarray()
print(encoded)
