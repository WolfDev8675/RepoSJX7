#!usr/bin/python
#
# *******
# **    Analysis 4:    
# *   Hourly sales activity like numvisits, totalamount per hour of day**
# *******
# **** Specific operation:  TotalCosts Hourly **** 
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

soln42={}          # final kv pairing and collecting results
for elem in data_dict:
    key=elem[0:13]
    if key.endswith(':'): key=elem[0:12]
    
    if key in soln42:
        soln42[key]=soln42[key]+data_dict[elem]
    else:
        soln42[key]=data_dict[elem]
        
# generating and printing results 
for elem in sorted(soln42):  
    print('%s\t%f'%(elem,soln42[elem]))
    
 

# end of code

##
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign4.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign4.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign4ex2.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign4ex2.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis4pmr/Job2 
# results obtained
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis4pmr/Job2/part* |head -n 10
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-11-19 21:13:25,308 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#2010-12-01 10   5235.810000
#2010-12-01 11   4234.160000
#2010-12-01 12   7447.920000
#2010-12-01 13   5063.540000
#2010-12-01 14   2831.220000
#2010-12-01 15   3587.310000
#2010-12-01 16   8623.140000
#2010-12-01 17   613.190000
#2010-12-01 8    1383.810000
#2010-12-01 9    7356.390000
#cat: Unable to write to output stream.
#kali@kali:~$ 
#
## *** restricting output to 10 outputs results in the cat error 
