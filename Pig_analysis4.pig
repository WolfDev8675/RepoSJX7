/* Analysis 4:
Hourly sales activity like numvisits, totalamount per hour of day. */

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
kv_asses41 = FOREACH data_cleaned GENERATE InvoiceDate,InvoiceNo; -- kv pair datetime to invoice
kv_asses41NR = DISTINCT kv_asses41; -- removing duplicates
soln41_prx = FOREACH kv_asses41NR GENERATE CONCAT((chararray)GetDay(InvoiceDate),'-',(chararray)GetMonth(InvoiceDate),'-',(chararray)GetYear(InvoiceDate),'->',(chararray)GetHour(InvoiceDate)) as (dayhr:chararray),InvoiceNo; --presolution 
soln41_grp = GROUP soln41_prx BY dayhr;  -- group 
soln41 = FOREACH soln41_grp GENERATE group as (dayhr:chararray),COUNT(soln41_prx.InvoiceNo);  -- final solution 

-- Job3 : TotalCost Monthly
kv_asses42 = FOREACH data_cleaned GENERATE InvoiceDate,(Quantity*UnitPrice) as (TotalCost:float); -- kv pair datetime to totalcost
soln42_prx = FOREACH kv_asses42 GENERATE CONCAT((chararray)GetDay(InvoiceDate),'-',(chararray)GetMonth(InvoiceDate),'-',(chararray)GetYear(InvoiceDate),'->',(chararray)GetHour(InvoiceDate)) as (dayhr:chararray),TotalCost; --presolution 
soln42_grp = GROUP soln42_prx BY dayhr;  -- group 
soln42 = FOREACH soln42_grp GENERATE group as (dayhr:chararray),SUM(soln42_prx.TotalCost);  -- final solution

-- 
--Storage 
STORE soln41 INTO '/home/kali/Hadoop/Results/pig_results/analysis4/Job1' USING PigStorage();
STORE soln42 INTO '/home/kali/Hadoop/Results/pig_results/analysis4/Job2' USING PigStorage();

-- end of code 

/*
** Results Obtained 
#**
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis4/Job1/part* | head -n 10
1-2-2011->8     2
1-2-2011->9     3
1-3-2011->8     4
1-3-2011->9     6
1-4-2011->8     2
1-4-2011->9     6
1-6-2011->7     2
1-6-2011->8     1
1-6-2011->9     3
1-7-2011->8     3
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis4/Job2/part* | head -n 10
1-2-2011->8     1110.6699995994568
1-2-2011->9     1342.5699996948242
1-3-2011->8     990.5500040054321
1-3-2011->9     4896.019991397858
1-4-2011->8     609.5900011062622
1-4-2011->9     2001.5900249481201
1-6-2011->7     326.899995803833
1-6-2011->8     1378.4800004959106
1-6-2011->9     1975.2699918746948
1-7-2011->8     961.8799977302551
kali@kali:~$ 

#**
*** only 10 results printed to avoid cluttering and scrolling outputs***
*/



