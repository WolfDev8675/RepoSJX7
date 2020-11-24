// Spark code for Analysis 6:  Find out the avg confirmed avg death avg active case month wise for India for state WestBengal

// prerun hive_preClean.hql file before running this file 

//cleaned data import 
var data_raw_cleaned= sc.textFile("hdfs://localhost:9000//assign3/clean_data/*")
var data_cleaned= data_raw_cleaned.map(x=>x.split("\t"))
data_cleaned.count // should hold value 107749 as is equal to as that in hive 

// data scheme: SNo, Last Update, Province, Country, Confirmed, Deaths, Recovered, Active
//analysis job
var precoll6=data_cleaned.filter(x=>{x(3)=="India" && x(2) =="West Bengal" && x(1) != ""}).map(x=>(x(1).substring(0,7),x(4).toInt,x(5).toInt,x(7).toInt)) // filter out requirements
var d2conf=precoll6.map(x=>(x._1,x._2)).reduceByKey(_+_).map(x=>(x._1,x._2.toFloat))  //totals
var d2dead=precoll6.map(x=>(x._1,x._3)).reduceByKey(_+_).map(x=>(x._1,x._2.toFloat))
var d2act=precoll6.map(x=>(x._1,x._4)).reduceByKey(_+_).map(x=>(x._1,x._2.toFloat))
var d2cts=sc.parallelize(precoll6.map(x=>(x._1,x._1)).countByKey().toSeq)   //counters   
var collconf=d2conf.join(d2cts).map{case (k,(v1,v2))=>(k,(v1/v2))}    // averages
var colldead=d2dead.join(d2cts).map{case (k,(v1,v2))=>(k,(v1/v2))}
var collact=d2act.join(d2cts).map{case (k,(v1,v2))=>(k,(v1/v2))}
var analysis6=collconf.join(colldead).join(collact).map{case (w,((x,y),z)) =>(w,(x,y,z))}  // final result 

// save
analysis6.saveAsTextFile("hdfs://localhost:9000/assign3/spark_jobs/analysis6")  

//end of code 

// Solution obtained:
//kali@kali:~$ hdfs dfs -cat /assign3/spark_jobs/analysis6/part* 
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-25 00:25:20,488 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(2020-07,(37955.418,1035.0,12953.129))
//(2020-08,(114114.97,2372.8064,25670.678))
//(2020-09,(196917.5,3847.75,24015.084))
//(2020-06,(13323.25,536.2,5242.15))
//kali@kali:~$ 
//
// ** solution in format (year-month,(average confirmed,average dead,average active))
