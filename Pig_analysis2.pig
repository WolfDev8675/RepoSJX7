/* Analysis 2:
Sales Metrics like NumCustomers, NumTransactions, AvgNumItems,
MinAmtperCustomer, MaxAmtperCustomer, AvgAmtperCustomer, StdDevAmtperCustomeretc. 
.. by country for top 5 countries  */

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
-- Job1
-- Number of Customers by Country for top 5
kvp_asgn2x1 = FOREACH data_cleaned GENERATE Country, CustomerID; -- kv map for generating number of customers
kvp_asgn2x1_NR = DISTINCT kvp_asgn2x1; -- non repetition ... removed all repitition of data from kvp_asgn2x1
resGrp2x1 = GROUP  kvp_asgn2x1_NR BY Country ; -- grouping by country 
resGrp2x1_final = FOREACH resGrp2x1 GENERATE group as (Country:chararray),COUNT(kvp_asgn2x1_NR.CustomerID) as (NumCust:int); --count of number of customers by country
ordered2x1 = ORDER resGrp2x1_final BY NumCust DESC; --ordering by descending order 
order2x1L5 = LIMIT ordered2x1 5;   -- top 5 values 
-- 
-- Job2
-- Number of Transactions by Country for top 5
kvp_asgn2x2 = FOREACH data_cleaned GENERATE Country, InvoiceNo; -- kv map for generating number of transactions
kvp_asgn2x2_NR = DISTINCT kvp_asgn2x2; -- non repetition ... removed all repitition of data from kvp_asgn2x2
resGrp2x2 = GROUP  kvp_asgn2x2_NR BY Country ; -- grouping by country  
resGrp2x2_final = FOREACH resGrp2x2 GENERATE group as (Country:chararray),COUNT(kvp_asgn2x2_NR.InvoiceNo) as (NTransact:int); --count of number of transactions by country
ordered2x2 = ORDER resGrp2x2_final BY NTransact DESC; --ordering by descending order 
order2x2L5 = LIMIT ordered2x2 5;   -- top 5 values 
-- 
-- Job3
-- Number of Average Number of Items by Country for top 5
kvp_asgn2x3 = FOREACH data_cleaned GENERATE Country, Quantity; -- kv map for generating number of transactions
resGrp2x3 = GROUP  kvp_asgn2x3 BY Country ; -- grouping by country  
resGrp2x3_final = FOREACH resGrp2x3 GENERATE group as (Country:chararray),SUM(kvp_asgn2x3.Quantity) as (TQuantity:int); --sum of number of items by country
ordered2x3 = ORDER resGrp2x3_final BY TQuantity DESC; --ordering by descending order 
order2x3L5x = LIMIT ordered2x3 5;   -- top 5 values total 
ctrCopy = FOREACH ordered2x3 GENERATE Country; -- creating copy of ordered2x3 for counter grouping 
ctrGrp = GROUP ctrCopy ALL; --grouped 
nosCtry = FOREACH ctrGrp GENERATE COUNT(ctrCopy.Country); -- total number of countries 
order2x3L5 = FOREACH order2x3L5x GENERATE Country as (Country:chararray), TQuantity*1.0/nosCtry as (AverageNos:float); -- final result 
--
--Job4 Job5 Job6
-- Minumum Amount Spent per Customer
kvp_asgn2x4CI = FOREACH data_cleaned GENERATE CustomerID,InvoiceNo;--kv map for Customer mapped to invoices ** contains duplicates 
kvp_asgn2x4IE = FOREACH data_cleaned GENERATE InvoiceNo as (InvoiceNo:chararray),UnitPrice*Quantity as (Expend:Float);--kv map for Invoices mapped to expenditures
resGrp2x4CI = DISTINCT kvp_asgn2x4CI; -- removing duplicates from customer-> invoice indexes


-- Storing the final results in respective locations pertaining to job
STORE order2x1L5 INTO '/home/kali/Hadoop/Results/pig_results/analysis2/Job1' USING PigStorage();
STORE order2x2L5 INTO '/home/kali/Hadoop/Results/pig_results/analysis2/Job2' USING PigStorage();
STORE order2x3L5 INTO '/home/kali/Hadoop/Results/pig_results/analysis2/Job3' USING PigStorage();
