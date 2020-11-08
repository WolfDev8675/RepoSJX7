#!usr/bin/python
#
# *******
# **    Analysis 2:    
# *    Reducer for calculating the results of                                                 **
# *   Sales Metrics like NumCustomers, NumTransactions, AvgNumItems,                          **
# *    MinAmtperCustomer, MaxAmtperCustomer, AvgAmtperCustomer.                               **
# *     by country for top 5 countries                                                        **
# *******
# **** Specific operation:  Sales Metric of Minimum Amount Spent Per Customer **** 
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
        print (" Input Data Error 1... -> Dictionary not generated or Inaccessible data list ")
        sys.exit(1)
#@print data_list       # debugging test code
#@print data_dict
resultsMIN={}       # dictionary for final tasks but dataset is expendable 
# segregating final informatics 
for customer in data_dict:
    # creating a workable dictionary for further Jobs
    resultsMIN[customer]=min(data_dict[customer].values())

resultsErosiv = resultsMIN # erosive dictionary for sort and print

#helping function
def maxElem(a={}):
    #function to find out maximum valued key
    key=a.keys()[0] #raw initialization
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
# end of job for analysis2 job4  

#@ are test lines for manual debugging codes

# end of code 

##
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign2.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign2.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign2ex4.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign2ex4.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis2pmr/Job4
# results obtained
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis2pmr/Job4/part*|head -n 10
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-11-08 11:20:04,268 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#12346   77183.600000
#15749   7837.500000
#12357   6207.670000
#12688   4873.810000
#12752   4366.780000
#18251   4314.720000
#12536   4161.060000
#12378   4008.620000
#15195   3861.000000
#12435   3850.900000
#cat: Unable to write to output stream.
#kali@kali:~$
#**..
#*** note that this job limited to 10 outputs from the head of the file systems in storage to avoid printing 4339 records cluttering the shell screen 
# ** this restriction imposed to limit output generated a cat error from the resulting stream 
