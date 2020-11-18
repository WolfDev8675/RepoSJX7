//Spark code for Analysis3: 
// **Daily sales activity like numvisits, totalamount monthly and quarterly for 1 year.
//cleaning of visible debris 
var data_raw= sc.textFile("hdfs://localhost:9000/assign1/OnlineRetail.txt")
var data_raw_split= data_raw.map(x=>x.split("\t"))
var data_headless=data_raw_split.mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter } 
data_headless.count
var data_cleaned=data_headless.filter{x=> if((x(3).toInt >=0 ) && (x(5).toFloat >=0.0) && (x(6)!=""))true else false}
data_cleaned.count
// cleaned data of primary debris 

//Analysis Job:
//Job1: Numvisits Monthly 
var kvp_dt2inv=data_cleaned.map(x=>{(x(4),x(0))}).distinct
var kv_grp31=kvp_dt2inv.map(x=>{(x._1.substring(5,7).toInt,x._2)}).groupByKey()
var soln31=kv_grp31.map(x=>{(x._1,x._2.size)}).sortBy(_._1)

//Job2: Numvisits quarterly
var kv_grp32=kvp_dt2inv.map(x=>{(((x._1.substring(5,7).toFloat-0.1)/3).toInt,x._2)}).groupByKey()
var soln32=kv_grp32.map(x=>{(x._1,x._2.size)}).sortBy(_._1)

//Job3: TotalCosts Monthly 
var kvp_dt2cost=data_cleaned.map(x=>{(x(4),(x(3).toInt*x(5).toFloat))})
var kv_grp33=kvp_dt2cost.map(x=>{(x._1.substring(5,7).toInt,x._2)}).groupByKey()
var soln33=kv_grp33.map(x=>{(x._1,x._2.sum)}).sortBy(_._1)

//Job4: TotalCosts Quarterly
var kv_grp34=kvp_dt2cost.map(x=>{(((x._1.substring(5,7).toFloat-0.1)/3).toInt,x._2)}).groupByKey()
var soln34=kv_grp34.map(x=>{(x._1,x._2.sum)}).sortBy(_._1)

//Save operations 
soln31.saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis3/Job1")
soln32.saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis3/Job2")
soln33.saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis3/Job3")
soln34.saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis3/Job4")

//end of code 


// Solutions Obtained 
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis3/Job1/part*
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-18 21:10:41,958 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(1,993)
//(2,1003)
//(3,1324)
//(4,1153)
//(5,1559)
//(6,1394)
//(7,1331)
//(8,1283)
//(9,1757)
//(10,1930)
//(11,2660)
//(12,2179)
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis3/Job2/part*
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-18 21:10:55,432 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(0,3320)
//(1,4106)
//(2,4371)
//(3,6769)
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis3/Job3/part*
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-18 21:11:03,089 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(1,569433.8)
//(2,447132.38)
//(3,595491.7)
//(4,469200.16)
//(5,678592.2)
//(6,661210.6)
//(7,600090.5)
//(8,645341.4)
//(9,952817.5)
//(10,1039277.94)
//(11,1161771.2)
//(12,1090883.8)
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis3/Job4/part*
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-18 21:11:11,186 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(0,1612100.4)
//(1,1809007.2)
//(2,2198295.5)
//(3,3292369.5)
//kali@kali:~$ 
//
