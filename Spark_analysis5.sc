//Spark code for Analysis5: 
// ** Basket size distribution (Note: Basket size = number of items in a transaction) *
// *  (in this questions, we would like to know that, number of transactions by each basket size *
// *   i.e. number of transactions with 3 size, number of transactions with 4 size etc.)  **
//cleaning of visible debris 
var data_raw= sc.textFile("hdfs://localhost:9000/assign1/OnlineRetail.txt")
var data_raw_split= data_raw.map(x=>x.split("\t"))
var data_headless=data_raw_split.mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter } 
data_headless.count
var data_cleaned=data_headless.filter{x=> if((x(3).toInt >=0 ) && (x(5).toFloat >=0.0) && (x(6)!=""))true else false}
data_cleaned.count
// cleaned data of primary debris 

//analysis jobs
// Job: Basket Size 
var kvp_asses5=data_cleaned.map(x=> {(x(0),x(3).toInt)})  // invoice mapped to quantity
var kvp_reduced=kvp_asses5.reduceByKey(_+_) // reduce to sum of quantity
var soln5=kvp_reduced.sortBy(_._2,false) // sorting and final solution 
soln5.saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis5") // store 

//end of code 


// Solutions Obtained 
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis5/part* | head -n 10
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-15 20:15:51,720 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(581483,80995)
//(541431,74215)
//(556917,15049)
//(563076,14730)
//(572035,13392)
//(567423,12572)
//(578841,12540)
//(552883,12266)
//(563614,12196)
//(562439,11848)
//cat: Unable to write to output stream.
//cat: Unable to write to output stream.
//kali@kali:~$ 

//
//***** note that for job the viewed results are limited to top 10 outputs to avoid printing all 18536 results ****
// ** this restriction imposed to limit output generated a cat error from the resulting stream 

