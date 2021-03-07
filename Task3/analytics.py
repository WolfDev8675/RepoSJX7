#!usr/bin/python
""" Analytics packaging to support with functions that help in 
analysing distribution nature of data in a pandas.Dataframe object 
 functions present : numericStrength, variety, reset_columnData
 """ 
# code: BishalBiswas(https://github.com/WolfDev8675)

#imports
import pandas as PD

# function definitions
def numericStrength(dSeries):
    """ Function numericStrength:
    operative: numericStrength(data_column as pandas.core.series.Series)
    returns the percentage of the data contained in the population is numeric 
    pointing in operator to take decision based on the majority value to set datatype """
    #...
    # initials 
    dSeries.to_list()
    numCounts=0
    elseCounts=0
    # finding numeric hits 
    for element in dSeries:
        if(type(element)==str):
            if element.isnumeric(): numCounts+=1
            else: elseCounts+=1
        else:
            if (type(element)==int or type(element)==float): numCounts+=1
            else: elseCounts+=1
    # end of for loop 
    #...  
    return (numCounts*100.0)/len(dSeries)  #final return 
# end of function 

def variety(dSeries,cutoff):
    """ Function variety:
    operative: variety(data_column as pandas.core.series.Series,cutoff value to determine number of classes(percentage))
    returns the percentage of the variations contained in the data 
    pointing in operator to take decision based on the types to set datatype 
    complete return type: list of mixed datatypes
    list[0] = dictionary of the percentage of occurances with classes
    list[1] = number of variation classes
    list[2] = classification of nature based on cutoff value ( categorized or randomized )
    classification calculation:
     percentage of difference between the data length and the number of categories generated 
     if found greater than cutoff, then it is inferred as categorised 
     else assumed as randomized distribution 
    ... 
    """
    #...
    #intitals
    dSeries.to_list()
    variations={}
    total_length=len(dSeries)
    ret_ls=[]
    cf_dec=(cutoff*1.0)/100
    # 
    for element in dSeries:
        if element not in variations: variations[element]=1
        else: variations[element]+=1
    # size class
    for element in variations:
        variations[element]=(variations[element]*100.0)/total_length
    #finalizing results
    ret_ls.append(variations)
    ret_ls.append(len(variations))
    # defining classification
    per_diff=(total_length-len(variations))*1.0/len(dSeries)
    if (per_diff>cf_dec): ret_ls.append('categorized')
    else: ret_ls.append('randomized')

    return ret_ls  # final return 
# end of function

def reset_columnData(dFrame=None,typing=None):
    """ Function reset_columnData(Pandas.Dataframe,{Column_name:Datatype_to_finalize})
    returns dataframe with datatypes changed and fixed according to typing information for the columns
    dFrame: defaults=None; possible values Pandas.Dataframe object
    typing: defaults=None; possible values 'category', 'numerical', 'object'
    
    returns: None; if any or both arguments are 'None';
    or pandas.Dataframe object with the changes made to the respective datatypes of columns

    """
    # empty handler 
    if (dFrame is None or typing is None):
        return None
    # inititalizing setup
    WorkerDFrame=dFrame
    # handling errors
    if type(dFrame) is not PD.DataFrame:
        raise ValueError(" dFrame must be a Pandas.DataFrame object")
    if type(typing) is not dict:
        raise ValueError(" Typing data must be a Dictionary ")
    # registering changes
    for cols in typing:
        if (typing[cols] == 'numerical'):
            WorkerDFrame[cols]=PD.to_numeric(WorkerDFrame[cols],errors='coerce')
        elif (typing[cols] == 'category'):
            WorkerDFrame=WorkerDFrame.astype({cols:typing[cols]})
        elif (typing[cols] == 'object'):
            WorkerDFrame=WorkerDFrame.astype({cols:typing[cols]})
        else:
            pass
    # end of loop 
    return WorkerDFrame #return changes
# end of function 

# end of codes
