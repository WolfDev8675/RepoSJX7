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
analysis5result = FOREACH kv_asses5 GENERATE InvoiceNo,SUM(Quantity);
