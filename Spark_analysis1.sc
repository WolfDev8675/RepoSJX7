// Spark code for Analysis 1:  Find the country with rising cases 

//Start of Code
//cleaning of visible debris 
var data_raw= sc.textFile("hdfs://localhost:9000/assign3/covid_19_data.csv")
var data_raw_split= data_raw.map(x=>x.split(","))
var data_headless=data_raw_split.mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter } 
data_headless.count
var data_cleaned=data_headless.filter{x=> if((x(3)!=""))true else false}
data_cleaned.count
var data_final=data_cleaned.map(x=>{x,x(5)-x(6)-x(7)})
