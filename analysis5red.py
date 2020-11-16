#!usr/bin/python
#
#   Analysis 5: 
#       Basket size distribution (Note: Basket size = number of items in a transaction) **
#       (in this questions, we would like to know that, number of transactions by each basket size) ** 
#       i.e. number of transactions with 3 size, number of transactions with 4 size etc. **
#
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
            # new found unique key :: invoice
            data_dict[elem[0]]=int(elem[1])
        else:
            #  already available country key
            data_dict[elem[0]] = data_dict[elem[0]]+int(elem[1])
        
    except Exception:
        print (" Input Data Error ... -> Dictionary not generated or In-accessable data list ")
       
sorted_dc= sorted(data_dict.items(),key = lambda kv:(kv[1],kv[0]),reverse=True)
for unit in sorted_dc:
    print('%s\t%d'%unit) 
#

# ** end of code 

##
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign5.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign5.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign5.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign5.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis5pmr
# results obtained
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis5pmr/part* |head -n 10
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-11-16 10:50:11,714 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#581483  80995
#541431  74215
#556917  15049
#563076  14730
#572035  13392
#567423  12572
#578841  12540
#552883  12266
#563614  12196
#562439  11848
#cat: Unable to write to output stream.
#kali@kali:~$ 

#***** note that for job the viewed results are limited to top 10 outputs to avoid printing all 18536 results ****
# ** this restriction imposed to limit output generated a cat error from the resulting stream 


