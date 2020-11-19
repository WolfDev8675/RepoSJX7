#!usr/bin/python
#
# *******
# **    Analysis 3:    
# *   Daily sales activity like numvisits, total amount monthly and quarterly for 1 year.**
# *******
# **** Specific operation:  Number Visits Quarterly **** 
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

soln32={}          # final kv pairing and collecting results
for elem in data_collect:
    key=int((float(elem[0][5:7])-0.1)/3)
    if key in soln32:
        soln32[key].append(elem[1])
    else:
        soln32[key]=[elem[1]]
        
# generating and printing results 
for elem in sorted(soln32):  
    print('%s\t%d'%(elem,len(soln32[elem])))
    
 

# end of code

##
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign3.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign3.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign3ex2.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign3ex2.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis3pmr/Job2
# results obtained
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis3pmr/Job2/part*
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-11-19 20:47:13,092 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#0       3320
#1       4106
#2       4371
#3       6769
#kali@kali:~$ 
##

