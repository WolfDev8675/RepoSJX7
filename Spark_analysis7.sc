// Analysis 7: 
// ** Customer Lifetime Value distribution by intervals of 1000’s (Customer Life time Value = total spend by customer in his/her tenure with the company) *
// * (In this question, we would like to calculate how many customers with CLV between 1-1000, 1000-2000 etc.). *
// * Please note that we don’t want calculate bins manually and it required to create bins dynamically. **

//Start of Code
//cleaning of visible debris 
var data_raw= sc.textFile("hdfs://localhost:9000/assign1/OnlineRetail.txt")
var data_raw_split= data_raw.map(x=>x.split("\t"))
var data_headless=data_raw_split.mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter } 
data_headless.count
var data_cleaned=data_headless.filter{x=> if((x(3).toInt >=0 ) && (x(5).toFloat >=0.0) && (x(6)!=""))true else false}
data_cleaned.count
// cleaned data of primary debris 

// analysis job
var kvp_asses7=data_cleaned.map(x=> {(x(6),x(3).toInt * x(5).toFloat)}) // primary collect
var kvp_clv=kvp_asses7.reduceByKey(_+_) //calculating clv   
var lolimit_cvl=kvp_clv.map(x=>{((x._2.toInt/1000)*1000,x._2)}) // limit specified map 
var grouped_cvl=lolimit_cvl.sortByKey().groupByKey()    // sort and group 
var soln7=grouped_cvl.map(x=>{(x._1,x._1.toInt +1000,x._2.size)}).sortBy(_._1) // final result sorted 
soln7.saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis7")  //storage 

//end of code 


// Solutions Obtained 
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis7/part* | head -n 10
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-16 02:43:12,748 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(0,1000,2671)
//(1000,2000,765)
//(2000,3000,347)
//(3000,4000,182)
//(4000,5000,99)
//(5000,6000,66)
//(6000,7000,46)
//(7000,8000,26)
//(8000,9000,19)
//(9000,10000,14)
//cat: Unable to write to output stream.
//kali@kali:~$ 

//***** note that for job the viewed results are limited to top 10 outputs to avoid printing all results max(cvl)=280206.03  ****
// ** this restriction imposed to limit output generated a cat error from the resulting stream 
