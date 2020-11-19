#!usr/bin/python
#
# *******
# **    Analysis 3:    
# *   Daily sales activity like numvisits, total amount monthly and quarterly for 1 year.**
# *******
# **** Specific operation:  TotalCosts Monthly **** 
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

soln33={}          # final kv pairing and collecting results
for elem in data_dict:
    key=int(elem[5:7])
    if key in soln33:
        soln33[key]=soln33[key]+data_dict[elem]
    else:
        soln33[key]=data_dict[elem]
        
# generating and printing results 
for elem in sorted(soln33):  
    print('%s\t%f'%(elem,soln33[elem]))
    
 

# end of code

##
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign3.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign3.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign3ex3.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign3ex3.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis3pmr/Job3 
# results obtained
##**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis3pmr/Job3/part*
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-11-19 20:58:21,152 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#1       569445.040000
#2       447137.350000
#3       595500.760000
#4       469200.361000
#5       678594.560000
#6       661213.690000
#7       600091.011000
#8       645343.900000
#9       952838.382000
#10      1039318.790000
#11      1161817.380000
#12      1090906.680000
#kali@kali:~$ 

#
#
