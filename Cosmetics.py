#!usr/bin/python
""" Cosmetics packaging to help with locating a file or a folder 
in a GUI manner using the Tkinter module of python native 
"""
# code: BishalBiswas(https://github.com/WolfDev8675)

#imports
from tkinter import filedialog
from tkinter import *
import pandas as PD
import pandastable as PTS

def uiGetFile(paths=None):
    """ function"""
    root=Tk()
    fBox=filedialog
    root.wm_title(" Get File: Native")
    files=fBox.askopenfile()
    root.destroy()
    return files.name

def showTablehead(dataFrame,windowName):
    """ function """
    root=Tk()
    root.wm_title(windowName)
    root.geometry("1200x600")
    fR=Frame(root)
    fR.pack(fill='both',expand=True)
    tb=PTS.Table(fR,dataframe=dataFrame)
    tb.show()
    root.mainloop()

def showInformation(windowName,binderTexts):
    """ function """
    root=Tk()
    root.wm_title(windowName)
    root.geometry("1200x600")
    tex=Text(root,width=500,height=1100)
    tex.pack()
    tex.insert(END,binderTexts)
    root.mainloop()
