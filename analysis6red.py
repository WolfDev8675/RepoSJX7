#!usr/bin/python
#
#   Analysis 6: 
#       Top 20 Items sold by frequency
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
       
sorted_dc= sorted(data_dict.items(),key = lambda kv:(kv[1],kv[0]),reverse=True)     # sorting  by descending order 
count=0   # counter 
for unit in sorted_dc:   # print top 20 
    if count<20:
        print('%s\t%d'%unit)
        count=count+1
    else: break 
#

# ** end of code 

##
# Operation using Hadoop MapReduce core -> 
# command operated on complete file OnlineRetail.txt
# hdfs operative command
#hadoop jar /$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign6.py -mapper "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/MapAsign6.py" -file /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign6.py -reducer "python /home/kali/KomodoIDE/Komodo_jobs/Assign1/RedAsign6.py" -input /assign1/OnlineRetail.txt -output /assign1/pythonMR_jobs/analysis6pmr
# results obtained
#**..
#kali@kali:~$ hdfs dfs -cat /assign1/pythonMR_jobs/analysis6pmr/part*
#Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
#2020-11-16 11:41:10,404 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
#23843->"PAPER CRAFT , LITTLE BIRDIE"    80995
#23166->MEDIUM CERAMIC TOP STORAGE JAR   77916
#84077->WORLD WAR 2 GLIDERS ASSTD DESIGNS        54415
#85099B->JUMBO BAG RED RETROSPOT 46181
#85123A->WHITE HANGING HEART T-LIGHT HOLDER      36725
#84879->ASSORTED COLOUR BIRD ORNAMENT    35362
#21212->PACK OF 72 RETROSPOT CAKE CASES  33693
#22197->POPCORN HOLDER   30931
#23084->RABBIT NIGHT LIGHT       27202
#22492->MINI PAINT SET VINTAGE   26076
#22616->PACK OF 12 LONDON TISSUES        25345
#21977->PACK OF 60 PINK PAISLEY CAKE CASES       24264
#17003->BROCADE RING PURSE       22963
#22178->VICTORIAN GLASS HANGING T-LIGHT  22433
#15036->ASSORTED COLOURS SILK FAN        21876
#21915->RED  HARMONICA IN BOX    20975
#22386->JUMBO BAG PINK POLKADOT  20165
#22197->SMALL POPCORN HOLDER     18252
#20725->LUNCH BAG RED RETROSPOT  17697
#84991->60 TEATIME FAIRY CAKE CASES      17689
#kali@kali:~$ 
#
#**
