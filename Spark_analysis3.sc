// Analysis 3: 
//  Select any year for which data is available: 
// For the selected year, create a table that contains data only for those stocks that have an average total traded quntity of 3 lakhs or more per day.
// Print out the first 25 entries of the table and submit.
// From above output, select any 10 stocks from IT ('HCLTECH', 'NIITTECH', 'TATAELXSI','TCS', 'INFY', 'WIPRO', 'DATAMATICS','TECHM','MINDTREE' and 'OFSS')
// and create a table combining their data. Find out the Pearsons Correlation Coeffecient for every pair of stocks you have selected above. 
//Final output should be in decreasing order of the coeffecient

//Start of Code
//cleaning of visible debris 
//import
var data_raw= sc.textFile("hdfs://localhost:9000/assign2/FINAL_FROM_DF.csv") 
var data_split=data_raw.map(x=>x.split(',')) //split by csv terms
var data_headless=data_split.mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter } //removing header line
data_headless.count // count confirm by 846404

//visible debris not noted ->  no additional filters imposed

//analysis job 
// 
var preset31=data_headless.filter{x=> if(x(10).substring(0,4).toInt == 2017) true else false}   // prefilter by year = 2017
var anlysjob3a=preset31.filter{x=> if(x(9).toFloat>=300000) true else false}    // filter by tottdrval>=300000
var res1x=anlysjob3a.take(25)  //submit as in question 
sc.parallelize(res1x).saveAsTextFile("hdfs://localhost:9000/assign2/spark_jobs/analysis3/Job1")
var anlysjob3b=anlysjob3a.filter{x=> if(x(0) =="HCLTECH" || x(0) == "NIITTECH" || x(0) == "TATAELXSI" || x(0) == "TCS" || x(0) == "INFY" || x(0) == "WIPRO" || x(0) == "DATAMATICS" || x(0) == "TECHM" || x(0) == "MINDTREE" || x(0) == "OFSS") true else false}
var it3left=anlysjob3b.map(x=>(x(0),x(5).toFloat))
var it3right=anlysjob3b.map(x=>(x(0),x(5).toFloat))
var cross=it3left.cartesian(it3right)

