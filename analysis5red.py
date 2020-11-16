#!usr/bin/python
#
#   Analysis 5: 
#       Basket size distribution (Note: Basket size = number of items in a transaction) **
#       (in this questions, we would like to know that, number of transactions by each basket size) ** 
#       i.e. number of transactions with 3 size, number of transactions with 4 size etc. **
#
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
            # new found unique key :: invoice
            data_dict[elem[0]]=int(elem[1])
        else:
            #  already available country key
            data_dict[elem[0]] = data_dict[elem[0]]+int(elem[1])
        
    except Exception:
        print (" Input Data Error ... -> Dictionary not generated or In-accessable data list ")
       
sorted_dc= sorted(data_dict.items(),key = lambda kv:(kv[1],kv[0]))
for unit in sorted_dc:
    print('%s\t%d'%unit) 

#end of code 
