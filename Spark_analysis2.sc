//Spark code for Analysis2: 
// Sales Metrics like NumCustomers, NumTransactions, AvgNumItems, MinAmtperCustomer, MaxAmtperCustomer, AvgAmtperCustomer. .. by country for top 5 countries 

//cleaning of visible debris 
var data_raw= sc.textFile("hdfs://localhost:9000/assign1/OnlineRetail.txt")
var data_raw_split= data_raw.map(x=>x.split("\t"))
var data_headless=data_raw_split.mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter } 
data_headless.count
var data_cleaned=data_headless.filter{x=> if((x(3).toInt >=0 ) && (x(5).toFloat >=0.0) && (x(6)!=""))true else false}
data_cleaned.count
// cleaned data of primary debris 

//analysis jobs

//process 1: number of customers by countries for top 5 
var cust2ctry_dup=data_cleaned.map(x=> {(x(7), x(6), 1)}) //customer id mapped to country::  contains duplicates
var cust2ctry=cust2ctry_dup.distinct  //removed duplicates
var kvp_cust2ctry=cust2ctry.map(x=> {(x._1, x._3)})  // map out occurences
var num_cust=kvp_cust2ctry.reduceByKey((a,b)=>(a+b))  // country to number of customers :: frequency
var num_cust_sorted=num_cust.sortBy(_._2,false)    // sort   
var soln1=num_cust_sorted.take(5) // result1

//process 2: number of transactions by countries for top 5
var inv2ctry_dup=data_cleaned.map(x=> {(x(7), x(0), 1)}) // invoice mapped to country ::  contains duplicates
var inv2ctry=inv2ctry_dup.distinct //removed duplicates
var kvp_inv2ctry=inv2ctry.map(x=> {(x._1, x._3)}) //map out occurences
var num_tran=kvp_inv2ctry.reduceByKey((a,b)=>(a+b)) // country to number of transactions :: frequency 
var num_tran_sorted=num_tran.sortBy(_._2,false)  //sort
var soln2=num_tran_sorted.take(5) //result2

//process 3: average number of items by country for top 5
var kvp_qty2ctry=data_cleaned.map(x=> {(x(7), x(3).toInt)}) //quantity mapped to country 
var kvp_tQ2ctry=kvp_qty2ctry.reduceByKey(_+_) // total quantity to each country 
var nosCtry=kvp_tQ2ctry.count // total number of countries 
var tQ_sorted=kvp_tQ2ctry.sortBy(_._2,false)  // sort 
var tQ_t5=tQ_sorted.take(5) // top 5 totals
var soln3_vec= {for(i <- 0 to 4) yield (tQ_t5(i)._1,tQ_t5(i)._2*1.0 /nosCtry)}  // calculating for the top 5 totals 
var soln3=soln3_vec.toArray  //result3

//process 4,5,6: Minimum, Maximum, Average amount per customers 
var inv2cost_nr = data_cleaned.map(x=>{(x(0),x(3). toInt * x(5).toFloat)})  // invoices mapped to the cost -- non reduced 
var inv2cust_dup=data_cleaned.map(x=>{(x(0),x(6))})  // invoices mapped to customers -- contains duplicates
var inv2cust=inv2cust_dup.distinct // removing duplicates 
var inv2cost=inv2cost_nr.reduceByKey(_+_) // summing up costs by invoices 
var mainCollect_join=inv2cust.join(inv2cost) // purposefully made invoice as the key since join works on K,V data inputs 
var cust2cost=mainCollect_join.map(x=> x._2) // customer mapped to costs incurred 
var cust2cost_grp=cust2cost.groupByKey() // group to create iterable set of costs 
var minCosts=cust2cost_grp.map(x=> (x._1,x._2.min))  // minimum costs per customers
var maxCosts=cust2cost_grp.map(x=> (x._1,x._2.max))  // maximum costs per customers
var avgCosts=cust2cost_grp.map(x=> (x._1,x._2.sum/x._2.size))  // average costs per customers 
var soln4=minCosts.sortBy(_._2,false) //sort descending   // result 4
var soln5=maxCosts.sortBy(_._2,false) //sort descending   // result 5
var soln6=avgCosts.sortBy(_._2,false) //sort descending   // result 6

// save operations 
sc.parallelize(soln1).saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis2/Job1")   // number of customers 
sc.parallelize(soln2).saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis2/Job2")   // number of transactions
sc.parallelize(soln3).saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis2/Job3")   // average number of items
soln4.saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis2/Job4")   // minimum payout per invoice
soln5.saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis2/Job5")   // maximum payout per invoice
soln6.saveAsTextFile("hdfs://localhost:9000/assign1/spark_jobs/analysis2/Job6")   // average payout per invoice 

//end of code 


// Solutions Obtained 
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis2/Job1/part*
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-06 13:45:31,716 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(United Kingdom,3921)
//(Germany,94)
//(France,87)
//(Spain,30)
//(Belgium,25)
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis2/Job2/part*
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-06 13:45:50,012 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(United Kingdom,16649)
//(Germany,457)
//(France,389)
//(EIRE,260)
//(Belgium,98)
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis2/Job3/part*
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-06 13:46:09,528 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(United Kingdom,115391.13513513513)
//(Netherlands,5430.72972972973)
//(EIRE,3797.972972972973)
//(Germany,3223.324324324324)
//(France,3012.7567567567567)
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis2/Job4/part*|head -n 10
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-06 13:46:34,308 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(12346,77183.59)
//(15749,7837.5)
//(12357,6207.6714)
//(12688,4873.8096)
//(12752,4366.78)
//(18251,4314.7197)
//(12536,4161.06)
//(12378,4008.6196)
//(15195,3861.0)
//(12435,3850.9)
//cat: Unable to write to output stream.
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis2/Job5/part*|head -n 10
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-06 13:47:02,137 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(16446,168469.6)
//(12346,77183.59)
//(15098,38970.0)
//(17450,31698.16)
//(12415,22775.93)
//(18102,22206.0)
//(15749,21535.9)
//(14646,20277.92)
//(12931,18841.48)
//(14156,16774.72)
//cat: Unable to write to output stream.
//cat: Unable to write to output stream.
//kali@kali:~$ hdfs dfs -cat /assign1/spark_jobs/analysis2/Job6/part*|head -n 10
//Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
//2020-11-06 13:47:20,295 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
//(16446,84236.25)
//(12346,77183.59)
//(15749,14844.767)
//(15098,13305.5)
//(12357,6207.6714)
//(12415,5948.3105)
//(12590,4932.1304)
//(12688,4873.8096)
//(12752,4366.78)
//(18102,4327.621)
//cat: Unable to write to output stream.
//cat: Unable to write to output stream.
//kali@kali:~$ 
/// 
//*** note that jobs 4, 5, 6, are limited to 10 outputs from the head of the file systems in storage to avoid printing 4339 records cluttering the shell screen 
// ** this restriction imposed to limit output generated a cat error from the resulting stream 
