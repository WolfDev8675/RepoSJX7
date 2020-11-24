// Spark code for Analysis 1:  Find the country with rising cases 

//Start of Code

// prerun hive_preClean.hql file before running this file 

//cleaned data import 
var data_raw_cleaned= sc.textFile("hdfs://localhost:9000//assign3/clean_data/*")
var data_cleaned= data_raw_cleaned.map(x=>x.split("\t"))
data_cleaned.count // should hold value 107749 as is equal to as that in hive 

// data scheme: SNo, Last Update, Province, Country, Confirmed, Deaths, Recovered, Active
//analysis job
var c2rec=data_cleaned.map(x=>(x(3),x(6).toInt)) //country->recovered
var c2act=data_cleaned.map(x=>(x(3),x(7).toInt)) //country->active
var rec_red=c2rec.reduceByKey(_+_)  //reduce by country
var act_red=c2act.reduceByKey(_+_)  //reduce by country
var preset1=rec_red.join(act_red)    //join by country 
var analysis1_uns=preset1.filter(x=>{x._2._1 < x._2._2}).map(x=>x._1)     // filter and map to output
var analysis1=analysis1_uns.sortBy[String]({x=>x})   // sort 

// save
analysis1.saveAsTextFile("hdfs://localhost:9000/assign3/spark_jobs/analysis1")  

//end of code 

// Solution obtained:
//kali@kali:~$ hdfs dfs -cat /assign3/spark_jobs/analysis1/part* |head -n 10
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-24 10:10:32,115 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
// Azerbaijan
//Angola
//Aruba
//Bahamas
//Belgium
//Belize
//Bolivia
//Botswana
//Burma
//Cape Verde
//cat: Unable to write to output stream.
//kali@kali:~$ 
//
