#!usr/bin/python
#
# *******
# **    Analysis 3:    
# *   Daily sales activity like numvisits, total amount monthly and quarterly for 1 year.**
# *******
# **** Specific operation:  TotalCosts Quarterly **** 
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
data_dict={}  # storing all costs
for elem in data_list:
    try:
        # test code for input errors
        if elem[0] not in data_dict:
            # new found unique key :: date
            data_dict[elem[0]]=int(elem[2])*float(elem[3])
        else:
            #  already available date key
            data_dict[elem[0]] = data_dict[elem[0]]+int(elem[2])*float(elem[3])
        
    except Exception:
         print (" Input Data Error ... -> Dictionary not generated or In-accessable data list ")
         sys.exit(1)

soln34={}          # final kv pairing and collecting results
for elem in data_dict:
    key=int((float(elem[5:7])-0.1)/3)
    if key in soln34:
        soln34[key]=soln34[key]+data_dict[elem]
    else:
        soln34[key]=data_dict[elem]
        
# generating and printing results 
for elem in sorted(soln34):  
    print('%s\t%f'%(elem,soln34[elem]))
    
 

# end of code

##
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign3.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign3.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign3ex4.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign3ex4.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis3pmr/Job4 
# results obtained
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis3pmr/Job4/part*
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-11-19 21:03:39,151 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#0       1612083.150000
#1       1809008.611000
#2       2198273.293000
#3       3292042.850000
#kali@kali:~$ 


#
