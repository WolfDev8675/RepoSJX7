// Spark code for Analysis 4:  In india find out the states where the death is highest

//Start of Code

// prerun hive_preClean.hql file before running this file 

//cleaned data import 
var data_raw_cleaned= sc.textFile("hdfs://localhost:9000//assign3/clean_data/*")
var data_cleaned= data_raw_cleaned.map(x=>x.split("\t"))
data_cleaned.count // should hold value 107749 as is equal to as that in hive 

// data scheme: SNo, Last Update, Province, Country, Confirmed, Deaths, Recovered, Active
//analysis job
var precoll4=data_cleaned.filter(x=>{x(3)=="India" && x(2) !=""}).map(x=>(x(2),x(5).toInt))  // filter by conditions and mapped as (state -> deaths)
var analysis4=precoll4.reduceByKey(_+_).sortBy(_._2,false) // reduce ,sort -> final result

// save
analysis4.saveAsTextFile("hdfs://localhost:9000/assign3/spark_jobs/analysis4")  

//end of code 

// Solution obtained:
//kali@kali:~$ hdfs dfs -cat /assign3/spark_jobs/analysis4/part* 
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-24 10:49:40,384 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(Maharashtra,1757974)
//(Tamil Nadu,457240)
//(Delhi,388327)
//(Karnataka,323412)
//(Gujarat,259068)
//(Uttar Pradesh,222519)
//(Andhra Pradesh,213593)
//(West Bengal,208712)
//(Madhya Pradesh,106583)
//(Punjab,87612)
//(Rajasthan,78890)
//(Telangana,59913)
//(Haryana,51992)
//(Jammu and Kashmir,45336)
//(Bihar,38665)
//(Odisha,27561)
//(Jharkhand,21734)
//(Assam,17956)
//(Chhattisgarh,17382)
//(Kerala,16691)
//(Uttarakhand,16450)
//(Puducherry,13232)
//(Goa,10614)
//(Tripura,6415)
//(Chandigarh,3483)
//(Himachal Pradesh,3007)
//(Andaman and Nicobar Islands,2009)
//(Manipur,1531)
//(Ladakh,1514)
//(Meghalaya,862)
//(Nagaland,543)
//(Arunachal Pradesh,451)
//(Sikkim,373)
//(Dadra and Nagar Haveli and Daman and Diu,143)
//(Unknown,0)
//(Dadar Nagar Haveli,0)
//(Mizoram,0)
//kali@kali:~$ 
//
// result is given as (state,deaths)
