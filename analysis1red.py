#!usr/bin/python
#
#   Analysis 1: 
#       Reducer for calculating value of Revenue Aggregate *
#           by country for top 5 countries  *
#               from mapper response        **

# ** start of code

import sys
from operator import itemgetter 
data_list=[]
for line in sys.stdin:
    data_line=line.strip()
    elements=data_line.split("\t")
    data_list.append(elements)  # generate local list
data_dict={}  # storing all revenue aggregates
for elem in data_list:
    if elem[0] not in data_dict:
        # new found unique key :: country
        data_dict[elem[0]]=float(elem[1])
    else:
        # already available country key
        data_dict[elem[0]] = data_dict[elem[0]]+float(elem[1])
#@print data_list
#helping function
def maxElem(a={}):
    #function to find out maximum valued key
    key=0 #raw initialization
    val=0
    for i in a:
        if a[i] > val:
            key=i
            val=a[i]
    # yielding results 
    return key
    #end of function
# finding top 5
data_dict_wk=data_dict
analysis1=[]
for i in range(5):
    t=maxElem(data_dict_wk)
    #@print t
    #@print data_dict_wk[t]
    val=data_dict_wk.pop(t)
    analysis1.append('%s\t%f'%(t,val))
    print('%s\t%f'%(t,val))

# end of job for analysis1  

#@ are test lines for manual debugging codes 


  
# ** end of code 
