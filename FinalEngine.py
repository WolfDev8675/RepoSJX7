#!usr/bin/python

# Code file: FinalEngine.py
# Task: 
##Final code to execute all processes sequentially in a manner as 
##required to complete the task  properly

# imports
from tkinter import *
import pandas as PD
import Cosmetics as CS

# Start of Code 

df1=PD.read_csv(CS.uiGetFile())
print(df1.head())
CS.showTablehead(df1,"datatable")

#rt3=Tk()
#rt3.wm_title('check3****')
#folds=fdgs.askdirectory()
#print(folds)
#rt3.mainloop()