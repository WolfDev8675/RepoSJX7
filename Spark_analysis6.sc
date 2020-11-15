// Analysis 6: 
// Top 20 Items sold by frequency 

//cleaning of visible debris 
var data_raw= sc.textFile("hdfs://localhost:9000/assign1/OnlineRetail.txt")
var data_raw_split= data_raw.map(x=>x.split("\t"))
var data_headless=data_raw_split.mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter } 
data_headless.count
var data_cleaned=data_headless.filter{x=> if((x(3).toInt >=0 ) && (x(5).toFloat >=0.0) && (x(6)!=""))true else false}
data_cleaned.count
// cleaned data of primary debris 

//analysis job
// Job: Top 20 items sold by frequency 
var kvp_asses6=data_cleaned.map(x=>{(x(1)+"->"+x(2),x(3).toInt)}) // mapping item type to quantity
var kvp_reduced=kvp_asses6.reduceByKey(_+_) //reduce to freq
var sort_res6=kvp_reduced.sortBy(_._2,false) //sort result by frequency
var soln6=sort_res6.take(20) //final result
sc.parallelize(soln6).saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis6")  // save 

//end of code 


// Solutions Obtained 
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis6/part*
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-15 21:31:52,078 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(23843->"PAPER CRAFT , LITTLE BIRDIE",80995)
//(23166->MEDIUM CERAMIC TOP STORAGE JAR,77916)
//(84077->WORLD WAR 2 GLIDERS ASSTD DESIGNS,54415)
//(85099B->JUMBO BAG RED RETROSPOT,46181)
//(85123A->WHITE HANGING HEART T-LIGHT HOLDER,36725)
//(84879->ASSORTED COLOUR BIRD ORNAMENT,35362)
//(21212->PACK OF 72 RETROSPOT CAKE CASES,33693)
//(22197->POPCORN HOLDER,30931)
//(23084->RABBIT NIGHT LIGHT,27202)
//(22492->MINI PAINT SET VINTAGE ,26076)
//(22616->PACK OF 12 LONDON TISSUES ,25345)
//(21977->PACK OF 60 PINK PAISLEY CAKE CASES,24264)
//(17003->BROCADE RING PURSE ,22963)
//(22178->VICTORIAN GLASS HANGING T-LIGHT,22433)
//(15036->ASSORTED COLOURS SILK FAN,21876)
//(21915->RED  HARMONICA IN BOX ,20975)
//(22386->JUMBO BAG PINK POLKADOT,20165)
//(22197->SMALL POPCORN HOLDER,18252)
//(20725->LUNCH BAG RED RETROSPOT,17697)
//(84991->60 TEATIME FAIRY CAKE CASES,17689)
//kali@kali:~$ 
//
//*****
//
