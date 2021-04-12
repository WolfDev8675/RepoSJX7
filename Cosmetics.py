#!usr/bin/python
""" Cosmetics packaging to help with locating a file or a folder,
showing data tables, important information, or taking decisions,
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
 
def selectFromLists(windowName,label1,listVAR1,label2=None,listVAR2=None):
    """ Function selectFromLists:
        Operation: select options from a list available ...    
        section 1 of this function fills window with checkboxes
        section 2 of this function fills window with radiobuttons
        ...
    """
    root=Tk()
    root.wm_title(windowName)
    root.geometry("1200x600")
    returns1=[];returns2=None;
    dctVAR={}
    dctVAR2=dict.fromkeys(listVAR1)
    if label2 is not None: dctVAR3=dict.fromkeys(listVAR2)
    for item in listVAR1:
        dctVAR[item]=IntVar()
    r=0
    c=0
    lb1=Label(root,text=label1).grid(row=r,columnspan=6,ipady=6);r+=1
    for item in listVAR1:
        dctVAR2[item]=Checkbutton(root,text=item,variable=dctVAR[item]).grid(row=r,column=c,ipadx=2)
        if c<6: c+=1
        else: c=0;r+=1
    r+=2   
    if label2 is not None:
        c=0
        lb2=Label(root,text=label2).grid(row=r,columnspan=6,ipady=6);r+=1
        response=StringVar()   
        for item in listVAR2:
            Radiobutton(root,text=item,variable=response,value=item).grid(row=r,column=c,ipadx=2)
            if c<6: c+=1
            else: c=0;r+=1
        returns2=response.get()
    b=Button(root,text='Confirm',command=root.destroy).grid(sticky=SW)
    root.mainloop()
    for item in dctVAR:
        dctVAR[item]=dctVAR[item].get()
        if dctVAR[item]: returns1.append(item)
    return [returns1,returns2]
    


 #** End of codes

#END OF FILE 'Cosmetics.py'