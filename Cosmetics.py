#!usr/bin/python
""" Cosmetics packaging to help with locating a file or a folder 
in a GUI manner using the Tkinter module of python native 
"""
# code: BishalBiswas(https://github.com/WolfDev8675)

#imports
from tkinter import filedialog,messagebox
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
 #end of function


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
  #end of function


def showInformation(windowName,binderTexts):
    """ Function  showInformation:
        Operation: use GUI to show information in the form of text """
    root=Tk()
    root.wm_title(windowName)
    root.geometry("1200x600")
    tex=Text(root,width=500,height=1100)
    tex.pack()
    tex.insert(END,binderTexts)
    root.mainloop()
  #end of function 

def decisionMessage(windowName,message):
    """ Function decisionMessage:
        Operation: show a message to the screen and ask to select either
        one of two options, by default command2 is selected """
    decision=False
    root=Tk()
    MsgBox=messagebox
    root.wm_title("Native Decision ")
    root.geometry("500x80")
    mbox=MsgBox.askquestion(windowName,message,icon='warning')
    root.destroy()
    if mbox=='yes': decision=True
    return decision
 #end of function 
    
    