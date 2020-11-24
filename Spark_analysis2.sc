// Spark code for Analysis 2:  Find the active case of top 5 country

//Start of Code

// prerun hive_preClean.hql file before running this file 

//cleaned data import 
var data_raw_cleaned= sc.textFile("hdfs://localhost:9000//assign3/clean_data/*")
var data_cleaned= data_raw_cleaned.map(x=>x.split("\t"))
data_cleaned.count // should hold value 107749 as is equal to as that in hive 

// data scheme: SNo, Last Update, Province, Country, Confirmed, Deaths, Recovered, Active
//analysis job
var c2act=data_cleaned.map(x=>(x(3),x(7).toInt)) //country->active
var act_red=c2act.reduceByKey(_+_)  //reduce by country
var analysis2=sc.parallelize(act_red.sortBy(_._2,false).take(5)) // final result 

// save
analysis2.saveAsTextFile("hdfs://localhost:9000/assign3/spark_jobs/analysis2")  

//end of code 

// Solution obtained:
//kali@kali:~$ hdfs dfs -cat /assign3/spark_jobs/analysis2/part* 
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-24 10:18:00,173 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(US,361485183)
//(Brazil,60868651)
//(India,60501744)
//(UK,40370420)
//(Russia,29711685)
//kali@kali:~$ 
//
//
