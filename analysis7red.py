#!usr/bin/python
#
#   Analysis 7: 
# ** Customer Lifetime Value distribution by intervals of 1000's (Customer Life time Value = total spend by customer in his/her tenure with the company) *
# * (In this question, we would like to calculate how many customers with CLV between 1-1000, 1000-2000 etc.). *
# * Please note that we don't want calculate bins manually and it required to create bins dynamically. **
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
      data_dict[elem[0]]=float(elem[1])
    else:
      #  already available country key
      data_dict[elem[0]] = data_dict[elem[0]]+float(elem[1])
        
  except Exception:
    print (" Input Data Error ... -> Dictionary not generated or In-accessable data list ")

collect_dict={}
for an_item in data_dict:
  if (int(data_dict[an_item])/1000)*1000 not in collect_dict:
    collect_dict[(int(data_dict[an_item])/1000)*1000]=[data_dict[an_item]]
  else: collect_dict[(int(data_dict[an_item])/1000)*1000].append(data_dict[an_item])

for unit in sorted(collect_dict):
  print ('%d\t%d\t%d'%(unit,unit+1000,len(collect_dict[unit])))
  
#

# ** end of code

##
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign7.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign7.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign7.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign7.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis7pmr
# results obtained
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis7pmr/part* | head -n 10 
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-11-16 21:02:48,834 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#0       1000    2671
#1000    2000    765
#2000    3000    347
#3000    4000    182
#4000    5000    99
#5000    6000    66
#6000    7000    46
#7000    8000    26
#8000    9000    19
#9000    10000   14
#kali@kali:~$ 

#***** note that for job the viewed results are limited to top 10 outputs to avoid printing all results max(cvl)=280206.03  ****
