// Analysis 2: 
//   Calculation of various statistical quantities and decision making: 
// Only lines with value "EQ" in the "series" column should be processed. 
// As the first stage, filter out all the lines that do not fulfil this criteria. 
// For every stock(with value "EQ" in the "series"), for every year, calculate the statistical parameters
// (Minimum, Maximum, Mean and Standard Deviation) and store the generated information in properly designated tables.


//Start of Code
//cleaning of visible debris 
//import
var data_raw= sc.textFile("hdfs://localhost:9000/assign2/FINAL_FROM_DF.csv") 
var data_split=data_raw.map(x=>x.split(',')) //split by csv terms
var data_headless=data_split.mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter } //removing header line
data_headless.count // count confirm by 846404

//visible debris not noted ->  no additional filters imposed
//Data Scheme: SYMBOL	SERIES	OPEN	HIGH	LOW	CLOSE	LAST	PREVCLOSE	TOTTRDQTY	TOTTRDVAL	TIMESTAMP	TOTALTRADES	ISIN


//analysis job 
// 
var precollect=data_headless.filter(x=>{x(1) == "EQ"})
var collectmap=precollect.map(x=>(x(10).substring(0,4),x(5).toDouble))
var groupedset=collectmap.groupByKey.map{ case (k,v)=>(k,v.min,v.max,v.mean,math.sqrt(v.variance))}
