#!usr/bin/python
#
# *******
# **    Analysis 3:    
# *   Daily sales activity like numvisits, total amount monthly and quarterly for 1 year.**
# *******
# **** Specific operation:  Number Visits Monthly **** 
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

soln31={}          # final kv pairing and collecting results
for elem in data_collect:
    key=int(elem[0][5:7])
    if key in soln31:
        soln31[key].append(elem[1])
    else:
        soln31[key]=[elem[1]]
        
# generating and printing results 
for elem in sorted(soln31):  
    print('%s\t%d'%(elem,len(soln31[elem])))
    
 

# end of code

##
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign3.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign3.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign3ex1.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign3ex1.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis3pmr/Job1
# results obtained
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis3pmr/Job1/part*
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#020-11-19 19:50:21,686 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#1       993
#2       1003
#3       1324
#4       1153
#5       1559
#6       1394
#7       1331
#8       1283
#9       1757
#10      1930
#11      2660
#12      2179
#kali@kali:~$ 
#
