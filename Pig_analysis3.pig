/* Analysis 3:
Daily sales activity like numvisits, totalamount monthly and quarterly for 1 year. */

-- start of code 

--raw data load with defined schema 
data_raw= LOAD '/home/kali/Hadoop/Local_Datasets/OnlineRetail.txt' USING PigStorage() as (InvoiceNo:chararray,StockCode:chararray,Description:chararray,Quantity:int,InvoiceDate:Datetime,UnitPrice:float,CustomerID:chararray,Country:chararray);
data_cleaned = FILTER data_raw BY (Quantity>=0 AND UnitPrice>=0.0 AND CustomerID!=''); --cleaning with condition 
ctrRawG= GROUP data_raw ALL;  -- grouping raw to count 
ctrClnG= GROUP data_cleaned ALL; -- grouping cleaned to count 
ctrRaw= FOREACH ctrRawG GENERATE COUNT(data_raw.Quantity);  --generating count raw 
ctrCln= FOREACH ctrClnG GENERATE COUNT(data_cleaned.Quantity); -- generating count cleaned 
-- dumping to trigger results' calculation
dump ctrRaw --value :: (541909)
dump ctrCln --value :: (397924)
-- cleaned of debris in data 

--analysis job 
-- Job1 : NumVisits Monthly
kv_asses31 = FOREACH data_cleaned GENERATE InvoiceDate,InvoiceNo; -- kv pair datetime to invoice
kv_asses31NR = DISTINCT kv_asses31; -- removing duplicates
soln31_prx = FOREACH kv_asses31NR GENERATE GetMonth(InvoiceDate) as (Month:int),InvoiceNo; --presolution 
soln31_grp = GROUP soln31_prx BY Month;  -- group 
soln31 = FOREACH soln31_grp GENERATE group as (Month:int),COUNT(soln31_prx.InvoiceNo);  -- final solution 

-- Job2 :  NumVisits Quarterly
soln32_prx = FOREACH kv_asses31NR GENERATE FLOOR((GetMonth(InvoiceDate)-0.1)/3) as (Quarter:int),InvoiceNo; --presolution 
soln32_grp = GROUP soln32_prx BY Quarter;  -- group 
soln32 = FOREACH soln32_grp GENERATE group as (Quarter:int),COUNT(soln32_prx.InvoiceNo);  -- final solution 

-- Job3 : TotalCost Monthly
kv_asses32 = FOREACH data_cleaned GENERATE InvoiceDate,(Quantity*UnitPrice) as (TotalCost:float); -- kv pair datetime to totalcost
soln33_prx = FOREACH kv_asses32 GENERATE GetMonth(InvoiceDate) as (Month:int),TotalCost; --presolution 
soln33_grp = GROUP soln33_prx BY Month;  -- group 
soln33 = FOREACH soln33_grp GENERATE group as (Month:int),SUM(soln33_prx.TotalCost);  -- final solution 

-- Job4 : TotalCost Quarterly
soln34_prx = FOREACH kv_asses32 GENERATE FLOOR((GetMonth(InvoiceDate)-0.1)/3) as (Quarter:int),TotalCost; --presolution 
soln34_grp = GROUP soln34_prx BY Quarter;  -- group 
soln34 = FOREACH soln34_grp GENERATE group as (Quarter:int),SUM(soln34_prx.TotalCost);  -- final solution 

-- 
--Storage 
STORE soln31 INTO '/home/kali/Hadoop/Results/pig_results/analysis3/Job1' USING PigStorage();
STORE soln32 INTO '/home/kali/Hadoop/Results/pig_results/analysis3/Job2' USING PigStorage();
STORE soln33 INTO '/home/kali/Hadoop/Results/pig_results/analysis3/Job3' USING PigStorage();
STORE soln34 INTO '/home/kali/Hadoop/Results/pig_results/analysis3/Job4' USING PigStorage();

-- end of code 

/*
** Results Obtained 
#**
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis3/Job1/part*
1       993
2       1003
3       1324
4       1153
5       1559
6       1394
7       1331
8       1283
9       1757
10      1930
11      2660
12      2179
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis3/Job2/part*
0       3320
1       4106
2       4371
3       6769
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis3/Job3/part*
1       569445.0322882384
2       447137.3490101546
3       595500.7586191893
4       469200.3588609899
5       678594.5577653646
6       661213.6881134436
7       600091.0089869479
8       645343.8979516104
9       952838.3793331122
10      1039318.7866888493
11      1161817.3760578
12      1090906.6718007103
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis3/Job4/part*
0       1612083.1399175823
1       1809008.6047397982
2       2198273.286271671
3       3292042.8345473595
kali@kali:~$ 

#**

*/


