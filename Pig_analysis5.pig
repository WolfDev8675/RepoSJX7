/* Analysis 5:
Basket size distribution (Note: Basket size = number of items in a transaction)
(in this questions, we would like to know that, number of transactions by each basket size
i.e. number of transactions with 3 size, number of transactions with 4 size etc.)*/
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
-- Job: Basket Size Distribution
kv_asses5 = FOREACH data_cleaned GENERATE InvoiceNo,Quantity; -- kv pair invoiceno to quantity
kv_asses5grp = GROUP kv_asses5 BY InvoiceNo;  -- grouping  
analysis5result = FOREACH kv_asses5grp GENERATE group as (InvoiceNo:chararray),SUM(kv_asses5.Quantity) as (Basket:int);  -- analysis result 
orderedRes5 = ORDER analysis5result BY Basket DESC; -- ordering by basket size
STORE orderedRes5 INTO '/home/kali/Hadoop/Results/pig_results/analysis5/' USING PigStorage();   -- storing 

-- end of code 

/*
** Results Obtained 
#** 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis5/part* | head -n 10 
581483  80995
541431  74215
556917  15049
563076  14730
572035  13392
567423  12572
578841  12540
552883  12266
563614  12196
562439  11848
kali@kali:~$ 

#**
##   ***** note that for job the viewed results are limited to top 10 outputs to avoid printing all 18536 results ****
*/
