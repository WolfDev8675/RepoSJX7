//Spark code for Analysis3: 
// **Hourly sales activity like numvisits, totalamount per hour of day..
//cleaning of visible debris 
var data_raw= sc.textFile("hdfs://localhost:9000/assign1/OnlineRetail.txt")
var data_raw_split= data_raw.map(x=>x.split("\t"))
var data_headless=data_raw_split.mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter } 
data_headless.count
var data_cleaned=data_headless.filter{x=> if((x(3).toInt >=0 ) && (x(5).toFloat >=0.0) && (x(6)!=""))true else false}
data_cleaned.count
// cleaned data of primary debris 

//Analysis Job:
//Job1: Numvisits Hourly
var kvp_dt2inv=data_cleaned.map(x=>{(x(4),x(0))}).distinct
var kv_grp41=kvp_dt2inv.map(x=>{(x._1.substring(0,13),x._2)}).groupByKey()
var soln41=kv_grp41.map(x=>{(x._1,x._2.size)}).sortBy(_._1)

//Job2: TotalCosts Hourly 
var kvp_dt2cost=data_cleaned.map(x=>{(x(4),(x(3).toInt*x(5).toFloat))})
var kv_grp42=kvp_dt2cost.map(x=>{(x._1.substring(0,13),x._2)}).groupByKey()
var soln42=kv_grp42.map(x=>{(x._1,x._2.sum)}).sortBy(_._1)
//Save operations 
soln41.saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis4/Job1")
soln42.saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis4/Job2")

//end of code 


// Solutions Obtained 
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis4/Job1/part* | head -n 10
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-18 21:23:48,011 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(2010-12-01 10,11)
//(2010-12-01 11,12)
//(2010-12-01 12,22)
//(2010-12-01 13,12)
//(2010-12-01 14,8)
//(2010-12-01 15,14)
//(2010-12-01 16,17)
//(2010-12-01 17,4)
//(2010-12-01 8:,6)
//(2010-12-01 9:,16)
//cat: Unable to write to output stream.
//cat: Unable to write to output stream.
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis4/Job2/part* | head -n 10
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-18 21:24:04,308 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(2010-12-01 10,5235.8096)
//(2010-12-01 11,4234.157)
//(2010-12-01 12,7447.928)
//(2010-12-01 13,5063.5415)
//(2010-12-01 14,2831.2178)
//(2010-12-01 15,3587.3083)
//(2010-12-01 16,8623.145)
//(2010-12-01 17,613.19)
//(2010-12-01 8:,1383.8099)
//(2010-12-01 9:,7356.3896)
//cat: Unable to write to output stream.
//cat: Unable to write to output stream.
//kali@kali:~$ 
//
// results limited to prevent decluttering of screen as a result the cat error is genererated
