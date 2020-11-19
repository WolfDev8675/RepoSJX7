#!usr/bin/python
#
# *******
# **    Analysis 4:    
# *   Hourly sales activity like numvisits, totalamount per hour of day.**
# *******
# **** Specific operation:  Number Visits Hourly **** 
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
data_collect=[]  # storing dictionary for all primary k-v sets 
for elem in data_list:
    try:
        # test code for input errors
        if (elem[0],elem[1]) not in data_collect:
            # new found unique key :: country
            data_collect.append((elem[0],elem[1]))
        # intake of unique key value sets
        
    except Exception:
         print (" Input Data Error ... -> Dictionary not generated or Inaccessible data list ")
         sys.exit(1)

soln41={}          # final kv pairing and collecting results
for elem in data_collect:
    key=elem[0][0:13]
    if key.endswith(':'): key=elem[0][0:12]
    
    if key in soln41:
      soln41[key].append(elem[1])
    else:
      soln41[key]=[elem[1]]
        
# generating and printing results 
for elem in sorted(soln41):  
    print('%s\t%d'%(elem,len(soln41[elem])))
    
#print data_collect

    

# end of code

##
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign4.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign4.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign4ex1.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign4ex1.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis4pmr/Job1 
# results obtained
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis4pmr/Job1/part* |head -n 10
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-11-19 21:09:42,483 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#2010-12-01 10   11
#2010-12-01 11   12
#2010-12-01 12   22
#2010-12-01 13   12
#2010-12-01 14   8
#2010-12-01 15   14
#2010-12-01 16   17
#2010-12-01 17   4
#2010-12-01 8    6
#2010-12-01 9    16
#kali@kali:~$ 

#
