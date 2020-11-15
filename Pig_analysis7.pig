/* Analysis 7:
Customer Lifetime Value distribution by intervals of 1000’s 
(Customer Life time Value = total spend by customer in his/her tenure with the company)
(In this question, we would like to calculate how many customers with CLV between 1-1000, 1000-2000 etc.).
Please note that we don’t want calculate bins manually and it required to create bins dynamically.*/
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
-- Job: Customer Lifetime Value distribution by intervals of 1000’s
kv_asses7 = FOREACH data_cleaned GENERATE CustomerID as (CustomerID:chararray), UnitPrice*Quantity as (TotalCost:float); -- for calculating costs 
kv_asses7grp = GROUP kv_asses7 BY CustomerID;
asses7collect = FOREACH kv_asses7grp GENERATE group as (CustomerID:chararray),SUM(kv_asses7.TotalCost) as (CLV:float);
asses7res = FOREACH asses7collect GENERATE ROUND(CLV)/1000*1000 as (LoValue:int),CLV;
asses7res_grp = GROUP asses7res BY LoValue;
asses7final = FOREACH asses7res_grp GENERATE group as (LoValue:int),(group + 1000) as (HiValue:int),COUNT(asses7res.CLV) as (Frequency:int);
order7res = ORDER asses7final BY LoValue;
STORE order7res INTO '/home/kali/Hadoop/Results/pig_results/analysis7/' USING PigStorage();   -- storing 

-- end of code 

/*
** Results Obtained 
#** 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis7/part* | head -n 10
0       1000    2671
1000    2000    765
2000    3000    347
3000    4000    182
4000    5000    99
5000    6000    66
6000    7000    46
7000    8000    26
8000    9000    19
9000    10000   14
kali@kali:~$ 


#**
## ***** note that for job the viewed results are limited to top 10 outputs to avoid printing all results max(cvl)=280206.03  ****
*/
