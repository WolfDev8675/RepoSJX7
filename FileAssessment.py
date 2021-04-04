#!usr/bin/python
 
#Code file: FileAssessment.py
#Task: 
#**  Show the details of the file received
#**  including the number of fields number of 
#**  record entries, null values
#**  type of fields and the boxplots


def FileAssessment(dFrame):
    typer0={}  # empty dictionaries for recognising data nature 
    typer1={}
    #establishing character of dataset
    for col in dFrame.columns:
        typer0[col]=[ALS.variety(dFrame[col],95)[2],ALS.numericStrength(dFrame[col])]
    # establishing fulfilment criteria of dataset 
    for element in typer0:
        if typer0[element][0].startswith('random'):  
            if typer0[element][1]>50: typer1[element]='numerical'
            else: typer1[element]='object'
        elif typer0[element][0].startswith('categ'): 
            typer1[element]='category'

    print