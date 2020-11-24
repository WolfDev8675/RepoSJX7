// Spark code for Analysis 3:  In India show the cases state wise no of confirmed and active

//Start of Code

// prerun hive_preClean.hql file before running this file 

//cleaned data import 
var data_raw_cleaned= sc.textFile("hdfs://localhost:9000//assign3/clean_data/*")
var data_cleaned= data_raw_cleaned.map(x=>x.split("\t"))
data_cleaned.count // should hold value 107749 as is equal to as that in hive 

// data scheme: SNo, Last Update, Province, Country, Confirmed, Deaths, Recovered, Active
//analysis job
var precoll3=data_cleaned.filter(x=>{x(3)=="India" && x(2) !=""}).map(x=>(x(2),x(6).toInt,x(7).toInt)) // filter out requirements
var recByState=precoll3.map(x=>(x._1,x._2))  // state -> recovered
var actByState=precoll3.map(x=>(x._1,x._3))  // state -> active 
var analysis3=((recByState.reduceByKey(_+_)).join(actByState.reduceByKey(_+_))).sortBy[String]({x=>x._1})   //reduce,join, sort 

// save
analysis3.saveAsTextFile("hdfs://localhost:9000/assign3/spark_jobs/analysis3")  

//end of code 

// Solution obtained:
//kali@kali:~$ hdfs dfs -cat /assign3/spark_jobs/analysis3/part* 
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-24 10:33:44,199 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(Andaman and Nicobar Islands,(117917,34108))
//(Andhra Pradesh,(17453162,5775776))
//(Arunachal Pradesh,(165642,80115))
//(Assam,(4801024,1494730))
//(Bihar,(6166710,1390568))
//(Chandigarh,(173468,96698))
//(Chhattisgarh,(1194704,941480))
//(Dadar Nagar Haveli,(2,20))
//(Dadra and Nagar Haveli and Daman and Diu,(111653,27596))
//(Delhi,(12067033,2037142))
//(Goa,(749105,263582))
//(Gujarat,(5455330,1289055))
//(Haryana,(3570722,918482))
//(Himachal Pradesh,(267595,134216))
//(Jammu and Kashmir,(1765177,799996))
//(Jharkhand,(1584397,718928))
//(Karnataka,(13116179,5914002))
//(Kerala,(2901357,1391503))
//(Ladakh,(131722,54691))
//(Madhya Pradesh,(3232615,986470))
//(Maharashtra,(36369938,15812141))
//(Manipur,(262065,125146))
//(Meghalaya,(68155,72760))
//(Mizoram,(36461,29196))
//(Nagaland,(153038,91432))
//(Odisha,(4453516,1463227))
//(Puducherry,(511847,234629))
//(Punjab,(2211207,887965))
//(Rajasthan,(4244075,1073416))
//(Sikkim,(61925,31845))
//(Tamil Nadu,(22809919,4851779))
//(Telangana,(5935753,1913481))
//(Tripura,(498075,267414))
//(Unknown,(0,233513))
//(Uttar Pradesh,(9752356,3604910))
//(Uttarakhand,(865723,403726))
//(West Bengal,(7619412,1878543))
kali@kali:~$ 
//
// result is given as (state,(recovered,active))
