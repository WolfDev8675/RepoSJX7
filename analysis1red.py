#!usr/bin/python
#
#   Analysis 1: 
#       Reducer for calculating value of Revenue Aggregate *
#           by country for top 5 countries  *
#               from mapper response        **

# ** start of code

import sys
from operator import itemgetter 
data_list=[]        # local list 
for line in sys.stdin:
    data_line=line.strip()      #remove whitespaces
    elements=data_line.split("\t")  #segregate components
    data_list.append(elements)  # generate local list
if len(data_list) is 0:
    print(" Input Stream Error ... -> Reducer didn't receive any data ")
    sys.exit(1)         # fatal error due to reducer not receiving any data
data_dict={}  # storing all revenue aggregates
for elem in data_list:
    try:
        # test code for input errors
        if elem[0] not in data_dict:
            # new found unique key :: country
            data_dict[elem[0]]=float(elem[1])
        else:
            #  already available country key
            data_dict[elem[0]] = data_dict[elem[0]]+float(elem[1])
        
    except Exception:
        print (" Input Data Error ... -> Dictionary not generated or In-accessable data list ")
        sys.exit(1)

#helping function
def maxElem(a={}):
    #function to find out maximum valued key
    key=0 #raw initialization
    val=0
    for i in a:
        if a[i] > val: #is greater than existing check
            key=i
            val=a[i]
    # returning result
    return key
    #end of function
    
# finding top 5
data_dict_wk=data_dict  # duplicating the dictonary to avoid original data distortion 
analysis1=[] # list to contain the results of the analysis1
for i in range(5):
    t=maxElem(data_dict_wk)     # max value containg key of the dictionary 
    try:
        # test removability of hashed data component
        val=data_dict_wk.pop(t)  # releasing the k,v pair from the disctionary
    except Exception:
        print ("  Data Error:: --> Inadequate availability  ")
        sys.exit(1)
       
    analysis1.append('%s\t%f'%(t,val))
    print('%s\t%f'%(t,val))

# end of job for analysis1  
  
# ** end of code 

