// Spark code for Analysis 1: Revenue Aggregate by country

//cleaning of visible debris 
var data_raw= sc.textFile("hdfs://localhost:9000/assign1/OnlineRetail.txt")
var data_raw_split= data_raw.map(x=>x.split("\t"))
var data_headless=data_raw_split.mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter } 
data_headless.count
var data_cleaned=data_headless.filter{x=> if((x(3).toInt >=0 ) && (x(5).toFloat >=0.0) && (x(6)!=""))true else false}
data_cleaned.count
// cleaned data of primary debris 

// analysis job 
var kvp_Asgn1=data_cleaned.map(x=> {(x(7),x(3).toInt,x(5).toFloat)})  // kv map for intake checking
kvp_Asgn1.take(5) //check kv maps
var kvp_final_Asgn1=data_cleaned.map(x=> {(x(7), x(3).toInt * x(5).toFloat)}) //final kv map for calculating aggregate
kvp_final_Asgn1.take(5) // checking multiplier value to kvp_Asgn1
var results=kvp_final_Asgn1.reduceByKey((i,j)=>(i+j)) //Revenue 
var res_sorted= results.sortBy(_._2,false) //arrange in descending order
sc.parallelize(res_sorted.take(5)).saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis1")

//end of code 
