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
var precollect=data_headless.filter(x=>{x(1) == "EQ"})  //task1
var collectmap=precollect.map(x=>(x(0)+"\t"+x(10).substring(0,4),x(5).toDouble))  //task2
var analysis2=collectmap.groupByKey.map{ case (k,v)=>(k,v.min,v.max,mean(v),math.sqrt(variance(v)))}.sortBy(_._1)  //task3 and final result
analysis2.saveAsTextFile("hdfs://localhost:9000/assign2/spark_jobs/analysis2")  //store 

// end of code 

//Result obtained :
//kali@kali:~$ hdfs dfs -cat /assign2/spark_jobs/analysis2/part* | head -n 10
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-26 19:28:57,232 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(20MICRONS      2016,25.45,43.15,32.56518218623481,4.449798961387773)
//(20MICRONS      2017,33.7,62.7,41.63407258064514,6.590982227296511)
//(3IINFOTECH     2016,3.8,6.8,5.012348178137656,0.7338403174843332)
//(3IINFOTECH     2017,3.7,8.0,4.663104838709679,0.7633751172614981)
//(3MINDIA        2016,9521.5,14939.55,12146.576923076926,1292.3010059868957)
//(3MINDIA        2017,10789.9,19366.4,13443.495967741936,1687.9086040389095)
//(5PAISA 2017,187.3,388.75,283.7261904761904,67.21481309780786)
//(63MOONS        2017,54.9,159.65,84.53957446808509,23.64905305624774)
//(8KMILES        2016,591.3,2483.7,1646.258299595143,541.7589089129798)
//(8KMILES        2017,369.5,987.9,613.172782258065,138.3271731430923)
//cat: Unable to write to output stream.
//cat: Unable to write to output stream.
//kali@kali:~$ 
//**
