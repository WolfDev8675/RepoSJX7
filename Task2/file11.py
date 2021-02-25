#!usr/bin/python
#
#Question: Code to operate on two data files provided 
# files kept localy at path: F:\BSE_2\VS_Reg_BSE\Task2 
# Read car data.csv and car condition.csv. Merge them together (files already provided).
#  Find out the following from the data set.
#   then perform the following tasks..
# 1. What is the size of the dataset? (row x column)
# 2. Data type of each of the columns and number of non-null values of each column.
# 3. How many outliers are there for each numerical column and what are their values?
# 4. Draw boxplot for each numerical column.

# Start of codes
#.. 

#imports
import pandas as PD
import numpy as NP
import matplotlib.pyplot as plotter

# data file access
rootpath=input("Please input the Path containg the Data ")
if rootpath=="" : rootpath="F:\BSE_2\VS_Reg_BSE\Task2\\"
file1name="car data.csv"
file2name="car condition.csv"

# Question 
with open(rootpath+"qs.txt") as qs:
    print(qs.read())

# Alignment marker 
print("\n\n")

# Dataframes 
cdcsv=PD.read_csv(rootpath+file1name)  # car data
cccsv=PD.read_csv(rootpath+file2name)  # car condition
print("Car data \n",cdcsv); print("Car condition \n",cccsv) 
# previous knowledge of datasets: both have 'car id' column 
c_mer=cccsv.merge(cdcsv,left_on='car id',right_on='car id')
print(c_mer)

# 1. Size of dataset 
print(" Question 1: ")
print(" Size of dataset (merged) :",c_mer.size)
dims=c_mer.shape
print(" Rows   \t:",dims[0],"\n Columns\t:",dims[1])

# Alignment marker 
print("\n\n")

# 2. Data type of each of the columns and number of non-null values of each column
# print(c_mer.dtypes) # .. not required as info does all the job
# info on the 
c_mer.info()

# Alignment marker 
print("\n\n")

# finding all column headers which have numerical values
col_list=[] # empty holder
for col in c_mer.columns:
    if(c_mer[col].dtype.name.startswith('int') | c_mer[col].dtype.name.startswith('float')):
        col_list.append(col) # append positives

# 3. Data type of each of the columns and number of non-null values of each column
print(" Searching and Printing Outliers in numerical columns ")
#Quartiles
for col in col_list:
    sort_col=sorted(c_mer[col].tolist())  #sorted values
    #Quartiles
    Q1=NP.percentile(sort_col,25,interpolation='midpoint') 
    # Q2=NP.percentile(sort_col,50,interpolation='midpoint') 
    Q3=NP.percentile(sort_col,75,interpolation='midpoint') 
    IQR=Q3-Q1 # Inter Quartile Range 
    # limits 
    Lower=Q1-1.5*IQR
    Upper=Q3+1.5*IQR
    # finding Outliers and printing where necessary
    print(" Outliers in Column : ",col)
    nos_Out=0 # counter for outliers
    for element in sort_col:
        if(element>Upper or element<Lower):
            nos_Out+=1
            if (nos_Out==1): print(" ",element,end=' ')
            else: print(",",element,end=' ')
    if nos_Out: print("\n\t",nos_Out," outliers found ")
    else: print(" No outliers found")

# Alignment marker 
print("\n\n")

# 4. Draw boxplot for each numerical column
# axis and position of subplots separate plots for each
axR=4;axC=4;pos=1;
plotter.figure(figsize=(13,7.5)).canvas.set_window_title(" BoxPlots of all numerical data ")
for col in col_list:
    plotter.subplot(axR,axC,pos)
    c_mer.boxplot(column=col)
    pos+=1
# all plots in one   
plotter.subplot(axR,axC,(pos,16))
c_mer.boxplot(column=col_list)
#final show 
plotter.show()