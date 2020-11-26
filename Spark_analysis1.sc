// Analysis 1: 
//  Use the given csv file as input data and implement following transformations: 
// a. Filter Rows on specified criteria "Symbol equals GEOMETRIC" 
// b. Select specific columns from those available: SYMBOL, OPEN, HIGH, LOW and CLOSE which meets above criteria 
// c. Generate count of the number of rows from above result


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
var analysisjob1a=data_headless.filter(x=>{x(0) == "GEOMETRIC"})  // option a
var analysisjob1b=analysisjob1a.map(x=>(x(0),x(2),x(3),x(4),x(5)))  // option b
var analysisjob1c=analysisjob1b.count // option c

// end of code 

//Result obtained :
//***
//.
//scala> analysisjob1c                                                                                                                                                                                                                       
//res87: Long = 295
//
//scala>     
//
//.*****

