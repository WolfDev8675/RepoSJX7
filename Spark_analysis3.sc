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
//Data Scheme: SYMBOL	SERIES	OPEN	HIGH	LOW	CLOSE	LAST	PREVCLOSE	TOTTRDQTY	TOTTRDVAL	TIMESTAMP	TOTALTRADES	ISIN

//operative methods 
import Numeric.Implicits._
def mean[T: Numeric](xs: Iterable[T]): Double = xs.sum.toDouble / xs.size      //mean
def variance[T: Numeric](xs: Iterable[T]): Double = {
  val avg = mean(xs)                                //variance
  xs.map(_.toDouble).map(a => math.pow(a - avg, 2)).sum / xs.size
}
def stdDev[T: Numeric](xs: Iterable[T]): Double = math.sqrt(variance(xs))         //standard deviation

//analysis job 
// 
var preset31=data_headless.filter{x=> if(x(10).substring(0,4).toInt == 2017) true else false}   // prefilter by year = 2017
var anlysjob3a=preset31.filter{x=> if(x(8).toFloat>=300000) true else false}    // filter by tottdrval>=300000
var res1x=anlysjob3a.take(25)  //submit as in question 
sc.parallelize(res1x).saveAsTextFile("hdfs://localhost:9000/assign2/spark_jobs/analysis3/Job1")
var anlysjob3b=anlysjob3a.filter{x=> if(x(0) =="HCLTECH" || x(0) == "NIITTECH" || x(0) == "TATAELXSI" || x(0) == "TCS" || x(0) == "INFY" || x(0) == "WIPRO" || x(0) == "DATAMATICS" || x(0) == "TECHM" || x(0) == "MINDTREE" || x(0) == "OFSS") true else false}
var it3left=anlysjob3b.map(x=>(x(0),x(5).toFloat))
var it3right=anlysjob3b.map(x=>(x(0),x(5).toFloat))
var cross=it3left.cartesian(it3right).map{case((a, b), (c, d))=>(a,c,b,d)}.filter{x=>(x._1 < x._2)}.map{case((a,b,c,d))=>(a+" , "+b ,c,d,c*d)} 
var gpsx_L=cross.map(x=>(x._1,x._2)).groupByKey  // iterable left  -> x
var gpsx_R=cross.map(x=>(x._1,x._3)).groupByKey  // iterable right -> y
var gpsx_C=cross.map(x=>(x._1,x._4)).groupByKey  // iterable center -> (x*y)
var joinback=gpsx_L.join(gpsx_R).join(gpsx_C)  // join back grouped iterables
var analysis3b_f=joinback.map{case(w, ((x, y), z))=> (w,(mean(z)-mean(x)*mean(y))/(stdDev(x)*stdDev(y)))}.sortBy(_._2,false)  // final operation
analysis3b_f.saveAsTextFile("hdfs://localhost:9000/assign2/spark_jobs/analysis3/Job2")  //store 

// end of code 

//Result obtained :
//kali@kali:~$ hdfs dfs -cat /assign2/spark_jobs/analysis3/Job2/part* | head -n 10
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-27 01:29:20,040 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(HCLTECH , OFSS,0.060179274588645304)
//(HCLTECH , INFY,0.03636273681709574)
//(HCLTECH , MINDTREE,0.03605078081500838)
//(HCLTECH , TCS,0.03148815953621653)
//(MINDTREE , OFSS,0.027856217844901495)
//(HCLTECH , NIITTECH,0.020602642393445326)
//(HCLTECH , TECHM,0.017544870699555067)
//(MINDTREE , TCS,0.01698240987202918)
//(MINDTREE , NIITTECH,0.009471649548329374)
//(MINDTREE , TECHM,0.008152816287473285)
//cat: Unable to write to output stream.
//cat: Unable to write to output stream.
//cat: Unable to write to output stream.
//kali@kali:~$ 
//

