// Spark code for Analysis 1: Revenue Aggregate by country

var data_raw=sc.textFile("hdfs://localhost:9000/assign1/OnlineRetail.txt")
data_raw.take(5)
var data_raw_split=data_raw.map(x=>x.split("\t"))
data_raw_split.take(4)
var data_headless=data_raw_split.mapPartitionsWithIndex{(idx,iter)=> if(idx==0)iter.drop(1)else iter}
var data_header=data_raw_split.take(1).flatMap(x=>x)
var data_framed=data_headless.toDF()

//not completed yet..
