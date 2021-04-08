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
    """ Function uiGetFile: 
        Operation: receive file path from user using GUI functionality"""
    root=Tk()
    fBox=filedialog
    root.wm_title(" Get File: Native")
    root.geometry("500x80")
    files=fBox.askopenfile()
    root.destroy()
    return files.name

def showTable(dataFrame,windowName):
    """ Function showTable:
        Operation: use GUI to preview a dataframe in the form of a table """
    root=Tk()
    root.wm_title(windowName)
    root.geometry("1200x600")
    fR=Frame(root)
    fR.pack(fill='both',expand=True)
    tb=PTS.Table(fR,dataframe=dataFrame)
    tb.show()
    root.mainloop()

def showInformation(windowName,binderTexts):
    """ Function  showInformation:
        Operation: use GUI to show information in the form of text """
    root=Tk()
    root.wm_title(windowName)
    root.geometry("1200x600")
    tex=Text(root,width=500,height=1100)
    tex.pack()
    #for components in binderTexts:
    #    tex.insert(END,components)
    tex.insert(END,binderTexts)
    root.mainloop()
