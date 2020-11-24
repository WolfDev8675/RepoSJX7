// Spark code for Analysis 5:  Find out the Avg confirmed Avg death Avg active case month wise for India
//Start of Code

// prerun hive_preClean.hql file before running this file 

//cleaned data import 
var data_raw_cleaned= sc.textFile("hdfs://localhost:9000//assign3/clean_data/*")
var data_cleaned= data_raw_cleaned.map(x=>x.split("\t"))
data_cleaned.count // should hold value 107749 as is equal to as that in hive 

// data scheme: SNo, Last Update, Province, Country, Confirmed, Deaths, Recovered, Active
//analysis job
var precoll5=data_cleaned.filter(x=>{x(3)=="India" && x(2) !="" && x(1) != ""}).map(x=>(x(1).substring(0,7),x(4).toInt,x(5).toInt,x(7).toInt)) // filter out requirements
var d2conf=precoll5.map(x=>(x._1,x._2)).reduceByKey(_+_).map(x=>(x._1,x._2.toFloat))  //totals
var d2dead=precoll5.map(x=>(x._1,x._3)).reduceByKey(_+_).map(x=>(x._1,x._2.toFloat))
var d2act=precoll5.map(x=>(x._1,x._4)).reduceByKey(_+_).map(x=>(x._1,x._2.toFloat))
var d2cts=sc.parallelize(precoll5.map(x=>(x._1,x._1)).countByKey().toSeq)   //counters   
var collconf=d2conf.join(d2cts).map{case (k,(v1,v2))=>(k,(v1/v2))}    // averages
var colldead=d2dead.join(d2cts).map{case (k,(v1,v2))=>(k,(v1/v2))}
var collact=d2act.join(d2cts).map{case (k,(v1,v2))=>(k,(v1/v2))}
var analysis5=collconf.join(colldead).join(collact).map{case (w,((x,y),z)) =>(w,(x,y,z))}  // final result 

// save
analysis5.saveAsTextFile("hdfs://localhost:9000/assign3/spark_jobs/analysis5")  

//end of code 

// Solution obtained:
//kali@kali:~$ hdfs dfs -cat /assign3/spark_jobs/analysis5/part* 
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-25 00:05:20,724 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(2020-07,(28480.818,712.83813,9836.423))
//(2020-08,(74345.87,1430.3638,18982.436))
//(2020-09,(133410.62,2217.3477,26609.49))
//(2020-06,(11390.59,352.1057,4755.6094))
//kali@kali:~$ 
//
// ** solution in format (year-month,(average confirmed,average dead,average active))
