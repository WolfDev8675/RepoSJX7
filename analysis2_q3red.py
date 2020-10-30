#!usr/bin/python
#
# *******
# **    Analysis 2:    
# *    Reducer for calculating the results of                                                  **
# *   Sales Metrics like NumCustomers, NumTransactions, AvgNumItems,                          **
# *    MinAmtperCustomer, MaxAmtperCustomer, AvgAmtperCustomer, StdDevAmtperCustomer, etc.    **
# *     by country for top 5 countries                                                        **
# *******
# **** Specific operation:  Sales Metric of Average Number of Items by country for top 5 **** 
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
        if elem[0] not in data_dict:
            # new found unique key :: country
            data_dict[elem[0]]=int(elem[2])
        else:
            #  already available country key
            data_dict[elem[0]]=data_dict[elem[0]]+int(elem[2])
        
    except Exception:
         print (" Input Data Error ... -> Dictionary not generated or Inaccessible data list ")
         sys.exit(1)
#@print data_list       # debugging test code
data_dict_res={}
tcountry =len(data_dict)
for member in data_dict:
    data_dict_res[member]=data_dict[member]*1.0/tcountry


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
data_dict_wk=data_dict_res
analysis2x3=[]
for i in range(5):
    t=maxElem(data_dict_wk)
    #@print t
    #@print data_dict_wk[t]
    try:
        # test removability of hashed data component
        val=data_dict_wk.pop(t)
    except Exception:
        print (" Data Error:: --> Inadequate availability  ")
        sys.exit(1)
    
    analysis2x3.append('%s\t%f'%(t,val))
    print('%s\t%f'%(t,val))

# end of job for analysis2 job3  

#@ are test lines for manual debugging codes 


  
# ** end of code 

##
# operation using linux core -> 
# command tested for a modified input file of 1000 datapoints from the original OnlineRetail.txt 
# linux core command  
# results obtained with command 
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/OnlRet_1K.txt | python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign2.py|sort|shuf| python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign2ex3.py
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-10-30 21:19:03,173 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#United Kingdom  3054.000000
#France  112.250000
#Australia       26.750000
#Netherlands     24.250000
# Data Error:: --> Inadequate availability  
#kali@kali:~$
##**..
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign2.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign2.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign2ex3.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign2ex3.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis2pmr/Job3
# results obtained
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis2pmr/Job3/part*
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-10-30 21:25:41,756 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#United Kingdom  115391.135135
#Netherlands     5430.729730
#EIRE    3797.972973
#Germany 3223.324324
#France  3012.756757
#kali@kali:~$ 
#**..

