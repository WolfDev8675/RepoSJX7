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

##
# operation using linux core -> 
# command tested for a modified input file of 1000 datapoints from the original OnlineRetail.txt 
# linux core command  
#hdfs dfs -cat /assign1/OnlRet_1K.txt | python /home/kali/KomodoIDE/Komodo_jobs/Assign1/analysis1map.py | sort| shuf  | python /home/kali/KomodoIDE/Komodo_jobs/Assign1/analysis1red.py
# results obtained 
#**..
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-10-22 03:28:09,071 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#United Kingdom  23099.540000
#France  855.860000
#Australia       358.250000
#Netherlands     192.600000
# Data Error:: --> Inadequate availability  
#kali@kali:~$ 
#**..
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign1.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign1.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign1.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign1.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis1pmr
# results obtained
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis1pmr/part*
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-10-26 21:18:02,723 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#United Kingdom  7308391.554004
#Netherlands     285446.340000
#EIRE    265545.900000
#Germany 228867.140000
#France  209024.050000
#kali@kali:~$ 
#**..
