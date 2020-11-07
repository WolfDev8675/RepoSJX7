#!usr/bin/python
#
# *******
# **    Analysis 2:    
# *    Reducer for calculating the results of                                                 **
# *   Sales Metrics like NumCustomers, NumTransactions, AvgNumItems,                          **
# *    MinAmtperCustomer, MaxAmtperCustomer, AvgAmtperCustomer.                               **
# *     by country for top 5 countries                                                        **
# *******
# **** Specific operation:  Sales Metric of Maximum Amount Spent Per Customer **** 
# start of code
import sys
from operator import itemgetter 
data_list=[]
for line in sys.stdin:
    data_line=line.strip()
    elements=data_line.split("\t")
    data_list.append(elements)  # generate local list
if len(data_list) == 0:
    print(" Input Stream Error ... -> Reducer didn't receive any data ")
    sys.exit(1)
data_dict={}  # storing dictionary for all primary k-v sets
for elem in data_list:
    try:
        # test code for input errors
        if elem[4] not in data_dict:
            # new customer found
            data_dict[elem[4]]={}
            data_dict[elem[4]][elem[1]]=int(elem[2])*float(elem[3])
        else:
            # customer exists
            if elem[1] in data_dict[elem[4]]:
                # invoice of the customer exists -> adding to the sum 
                data_dict[elem[4]][elem[1]]= data_dict[elem[4]][elem[1]]+int(elem[2])*float(elem[3])
            else:
                # invoice doesn't exists for the customer -> generating new invoice info
                data_dict[elem[4]][elem[1]]=int(elem[2])*float(elem[3])
    except Exception:
         print (" Input Data Error ... -> Dictionary not generated or Inaccessible data list ")
         sys.exit(1)
#@print data_list       # debugging test code
resultsMAX={}       # dictionary for final tasks but dataset is expendable 
# segregating final informatics 
for customer in data_dict:
    # creating a workable dictionary for further Jobs
    resultsMAX[customer]=max(data_dict[customer].values())

resultsErosiv = resultsMAX # erosive dictionary for sort and print 
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

# sort and print using erosive dictionary
steps=len(resultsErosiv)
for i in range(steps):
    t=maxElem(resultsErosiv)
    #@print t
    #@print resultsErosiv[t]
    try:
        # test removability of hashed data component
        val=resultsErosiv.pop(t)
    except Exception:
        print (" Data Error:: --> Inadequate availability  ")
        sys.exit(1)
    
    print('%s\t%f'%(t,val))
#
# end of job for analysis2 job5  

#@ are test lines for manual debugging codes

# end of code 
