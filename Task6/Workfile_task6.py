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
import matplotlib.pyplot as PLOT
import seaborn as SEA

# data file access
rootpath=input("Please input the Path containing the Data ")
if rootpath=="" : rootpath="data\\"
file1name="car data.csv"
file2name="car condition.csv"
try:
    # Question 
    with open(rootpath+"qsxd.txt") as qsxd:
        print(qsxd.read())
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

# All column names: to be used while referencing during plots
ColumnSet=list(typer1.keys())
# Removing possible columns that can be set as indexables  
# and segregating numericals and categorized sets 
#** Reasoning: Naming and indexing columns or identifier related  columns 
#cannot be plotted or will generate an effective but useless plot 
# ( /*. In this case, this particular section is targetted to remove 'car name' 
# and 'car id' since the datasets are fixed in the problem description, but,
#  specific cases may apply relative to different datasets)
indexable=ALS.detectKeys(c_mer_moded) # finding indexable columns
# removing indexable columns from graphable set 
for idx in indexable: 
    if idx in ColumnSet: ColumnSet.remove(idx)
# Segregation
numericals=[]
categoricals=[]
for column in ColumnSet:
    if(typer1[column] == 'numerical'): numericals.append(column)
    if(typer1[column] == 'category'): categoricals.append(column)

#   1. Plot bar chart, box-plot, violin plot, line plot.
print(" 1. Plot bar chart, box-plot, violin plot, line plot ")
MxCol=4
MxRws=5 # {two headers and two sets of plots (numerical and categorical)}
print('\n Bar plots ')
PLOT.figure(figsize=(13,7.5)).canvas.set_window_title(" Bar Plots ")
PLOT.subplot(MxRws,MxCol,(1,4));PLOT.axis("off");PLOT.grid("off");
PLOT.text(0.5,0.5,"Numericals",horizontalalignment='center',verticalalignment='center',fontsize=18)
pos=5 # set after the numericals header
for numberCol in numericals:
    PLOT.subplot(MxRws,MxCol,pos);c_mer_moded[numberCol].plot(kind='bar');PLOT.xscale('linear');pos+=1
    PLOT.title(numberCol);PLOT.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
PLOT.subplot(MxRws,MxCol,(13,16));PLOT.axis("off");PLOT.grid("off");
PLOT.text(0.5,0.5,"Categoricals",horizontalalignment='center',verticalalignment='center',fontsize=18)
pos=17 #reset after categoricals header
for catCol in categoricals:
    data_dist=ALS.variety(c_mer_moded[catCol],95)[0]
    if NP.nan in data_dist: data_dist['NULLS']=data_dist.pop(NP.nan)
    PLOT.subplot(MxRws,MxCol,pos);PLOT.bar(list(data_dist.keys()),list(data_dist.values()));pos+=1
    PLOT.title(catCol);PLOT.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
print(" Plot generated on the figure window ") #console interaction
PLOT.tight_layout();PLOT.show()

print('\n Box-plots ') 
PLOT.figure(figsize=(13,7.5)).canvas.set_window_title(" Box Plots ")
PLOT.subplot(MxRws,MxCol,(1,4));PLOT.axis("off");PLOT.grid("off");
PLOT.text(0.5,0.5,"Numericals",horizontalalignment='center',verticalalignment='center',fontsize=18)
pos=5 # set after the numericals header
for numberCol in numericals:
    PLOT.subplot(MxRws,MxCol,pos);c_mer_moded[numberCol].plot(kind='box');PLOT.xscale('linear');pos+=1
    PLOT.title(numberCol);PLOT.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
PLOT.subplot(MxRws,MxCol,(13,16));PLOT.axis("off");PLOT.grid("off");
PLOT.text(0.5,0.5,"Categoricals",horizontalalignment='center',verticalalignment='center',fontsize=18)
pos=17 #reset after categoricals header
for catCol in categoricals:
    PLOT.subplot(MxRws,MxCol,pos);c_mer_moded[catCol].cat.codes.plot(kind='box');PLOT.xscale('linear');pos+=1 
    PLOT.title(catCol);PLOT.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
print(" Plot generated on the figure window ") #console interaction
PLOT.tight_layout();PLOT.show()

print('\n Violin plots ') 
PLOT.figure(figsize=(13,7.5)).canvas.set_window_title(" Violin Plots ")
PLOT.subplot(MxRws,MxCol,(1,4));PLOT.axis("off");PLOT.grid("off");
PLOT.text(0.5,0.5,"Numericals",horizontalalignment='center',verticalalignment='center',fontsize=18)
pos=5 # set after the numericals header
for numberCol in numericals:
    PLOT.subplot(MxRws,MxCol,pos);SEA.violinplot(data=list(c_mer_moded[numberCol]));PLOT.xscale('linear');pos+=1
    PLOT.title(numberCol);PLOT.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
PLOT.subplot(MxRws,MxCol,(13,16));PLOT.axis("off");PLOT.grid("off");
PLOT.text(0.5,0.5,"Categoricals",horizontalalignment='center',verticalalignment='center',fontsize=18)
pos=17 #reset after categoricals header
for catCol in categoricals:
    PLOT.subplot(MxRws,MxCol,pos);SEA.violinplot(data=list(c_mer_moded[catCol].cat.codes));PLOT.xscale('linear');pos+=1
    PLOT.title(catCol);PLOT.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
print(" Plot generated on the figure window ") #console interaction
PLOT.tight_layout();PLOT.show()
#**** MATPLOTLIB trials errors
        #FGS,AXS= PLOT.subplots(2,1,figsize=(13,7.5))
        #AXS[0].violinplot(c_mer_moded[numericals].values.tolist());AXS[0].set_title(" Numericals ")
        #AXS[1].violinplot(c_mer_moded[categoricals].values.tolist());AXS[1].set_title("Categoricals")
        #FGS.canvas.set_window_title(" Violin Plots ");PLOT.tight_layout();PLOT.show()

print('\n Line plots ')
PLOT.figure(figsize=(13,7.5)).canvas.set_window_title(" Line Plots ");PLOT.subplot(MxRws,MxCol,(1,4));PLOT.axis("off");PLOT.grid("off");
PLOT.text(0.5,0.5,"Numericals",horizontalalignment='center',verticalalignment='center',fontsize=18)
pos=5 # set after the numericals header
for numberCol in numericals:
    PLOT.subplot(MxRws,MxCol,pos);c_mer_moded[numberCol].plot(kind='line');PLOT.xscale('linear');pos+=1
    PLOT.title(numberCol);PLOT.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
PLOT.subplot(MxRws,MxCol,(13,16));PLOT.axis("off");PLOT.grid("off");
PLOT.text(0.5,0.5,"Categoricals",horizontalalignment='center',verticalalignment='center',fontsize=18)
pos=17 #reset after categoricals header
for catCol in categoricals:
    PLOT.subplot(MxRws,MxCol,pos);c_mer_moded[catCol].cat.codes.plot(kind='line');PLOT.xscale('linear');pos+=1
    PLOT.title(catCol);PLOT.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
print(" Plot generated on the figure window ") #console interaction
PLOT.tight_layout();PLOT.show()

#   2. Build correlation matrix.
print(" 2. Build correlation matrix ")
print(c_mer_moded.corr())

#   3. Show distribution of data.
print(" 3. Show distribution of data ")
MxCol=3
MxRws=4 
PLOT.figure(figsize=(13,7.5)).canvas.set_window_title(" Overall Distribution ")
PLOT.subplot(MxRws,MxCol,(1,3));PLOT.axis("off");PLOT.grid("off");
info_str="All Columns (Numericals and Categoricals) \n Identifier columns omitted \n KDE Plots "
PLOT.text(0.5,0.5,info_str,horizontalalignment='center',verticalalignment='center',fontsize=18)
pos=4 # set after the numericals header
for numberCol in numericals:
    PLOT.subplot(MxRws,MxCol,pos);c_mer_moded[numberCol].plot(kind='kde')
    PLOT.xscale('linear');pos+=1;PLOT.title(numberCol)
    PLOT.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)

for catCol in categoricals:
    PLOT.subplot(MxRws,MxCol,pos);c_mer_moded[catCol].cat.codes.plot(kind='kde')
    PLOT.xscale('linear');pos+=1;PLOT.title(catCol)
    PLOT.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
print(" Plot generated on the figure window ") #console interaction
PLOT.tight_layout();PLOT.show()

#   4. Describe different statistics of data
print(" 4. Describe different statistics of data ")
print(c_mer_moded.describe())

# end of codes