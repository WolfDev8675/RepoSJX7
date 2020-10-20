//Spark code for Analysis2: 
// Sales Metrics like NumCustomers, NumTransactions, AvgNumItems, MinAmtperCustomer, MaxAmtperCustomer, AvgAmtperCustomer, StdDevAmtperCustomeretc. .. by country for top 5 countries 

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
//process 3: average number of items
var kvp_qty2ctry=data_cleaned.map(x=> {(x(7), x(3).toInt)}) //quantity mapped to country 
var kvp_tQ2ctry=qty2ctry.reduceByKey(_+_) // total quantity to each country 
var nosCtry=tQ2ctry.count // total number of countries 
var tQ_sorted=kvp_tQ2ctry.sortBy(_._2,false)  // sort 
var soln3_vec= {for(i <- 0 to 4) yield (tQ_sorted(i)._1,tQ_sorted(i)._2*1.0 /nosCtry)}  // calculating for the top 5 totals 
var soln3=soln3_vec.toArray  //result3
//process 4: 
