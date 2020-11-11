/* Analysis 2:
Sales Metrics like NumCustomers, NumTransactions, AvgNumItems,
MinAmtperCustomer, MaxAmtperCustomer, AvgAmtperCustomer. 
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
order2x1L5 = LIMIT ordered2x1 5;   -- top 5 values **-- final result job1
-- 
-- Job2
-- Number of Transactions by Country for top 5
kvp_asgn2x2 = FOREACH data_cleaned GENERATE Country, InvoiceNo; -- kv map for generating number of transactions
kvp_asgn2x2_NR = DISTINCT kvp_asgn2x2; -- non repetition ... removed all repitition of data from kvp_asgn2x2
resGrp2x2 = GROUP  kvp_asgn2x2_NR BY Country ; -- grouping by country  
resGrp2x2_final = FOREACH resGrp2x2 GENERATE group as (Country:chararray),COUNT(kvp_asgn2x2_NR.InvoiceNo) as (NTransact:int); --count of number of transactions by country
ordered2x2 = ORDER resGrp2x2_final BY NTransact DESC; --ordering by descending order 
order2x2L5 = LIMIT ordered2x2 5;   -- top 5 values **-- final result job2
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
nosCtry = FOREACH ctrGrp GENERATE COUNT(ctrCopy.Country) as (value:int); -- total number of countries 
order2x3L5 = FOREACH order2x3L5x GENERATE Country as (Country:chararray), TQuantity*1.0/(nosCtry.value) as (AverageNos:float); -- top 5 values **-- final result job3 
--
--Job4 Job5 Job6
-- Minimum, Maximum, Average amount per customers
kvp_asgn2x456CI = FOREACH data_cleaned GENERATE CustomerID,InvoiceNo;--kv map for Customer mapped to invoices ** contains duplicates 
kvp_asgn2x456IE = FOREACH data_cleaned GENERATE InvoiceNo as (InvoiceNo:chararray),UnitPrice*Quantity as (Expend:Float);--kv map for Invoices mapped to expenditures
resGrp2x456CI = DISTINCT kvp_asgn2x456CI; -- removing duplicates from customer-> invoice indexes
resGrp2x456IE_gp = GROUP kvp_asgn2x456IE BY InvoiceNo; -- pre grouping for calculating the sum total of an invoice bill
resGrp2x456IE = FOREACH resGrp2x456IE_gp GENERATE group as (InvoiceNo:chararray),SUM(kvp_asgn2x456IE.Expend) as (TotalAtInv:float); -- summing to total of every invoices
masterJoin2x456 = JOIN resGrp2x456IE BY InvoiceNo, resGrp2x456CI BY InvoiceNo; -- joining by common key -> viz, Invoice number 
masterCollect2x456 = FOREACH masterJoin2x456 GENERATE resGrp2x456CI::CustomerID as (CustomerID:chararray),resGrp2x456IE::TotalAtInv as (TotalCost:float); -- link customers to total costs at a invoice collection
masterGrp2x456 = GROUP masterCollect2x456 BY CustomerID; -- grouped to get the specific tasks done 
minCosts = FOREACH masterGrp2x456 GENERATE group as (CustomerID:chararray),MIN(masterCollect2x456.TotalCost) as (Minima:Float); -- job4 precursor
maxCosts = FOREACH masterGrp2x456 GENERATE group as (CustomerID:chararray),MAX(masterCollect2x456.TotalCost) as (Maxima:Float); -- job5 precursor
avgCosts = FOREACH masterGrp2x456 GENERATE group as (CustomerID:chararray),SUM(masterCollect2x456.TotalCost)/SIZE(masterCollect2x456.TotalCost) as (Average:Float); -- job6 precursor
order2x4 = ORDER minCosts BY Minima DESC;  -- descrnding order ** -- final result job4
order2x5 = ORDER maxCosts BY Maxima DESC;  -- descrnding order ** -- final result job5
order2x6 = ORDER avgCosts BY Average DESC;  -- descrnding order ** -- final result job6
--
-- Storing the final results in respective locations pertaining to job
STORE order2x1L5 INTO '/home/kali/Hadoop/Results/pig_results/analysis2/Job1' USING PigStorage();
STORE order2x2L5 INTO '/home/kali/Hadoop/Results/pig_results/analysis2/Job2' USING PigStorage();
STORE order2x3L5 INTO '/home/kali/Hadoop/Results/pig_results/analysis2/Job3' USING PigStorage();
STORE order2x4 INTO '/home/kali/Hadoop/Results/pig_results/analysis2/Job4' USING PigStorage();
STORE order2x5 INTO '/home/kali/Hadoop/Results/pig_results/analysis2/Job5' USING PigStorage();
STORE order2x6 INTO '/home/kali/Hadoop/Results/pig_results/analysis2/Job6' USING PigStorage();

-- end of code 

/*
** Results Obtained 
#** 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis2/Job1/part*
United Kingdom  3921
Germany 94
France  87
Spain   30
Belgium 25
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis2/Job2/part*
United Kingdom  16649
Germany 457
France  389
EIRE    260
Belgium 98
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis2/Job3/part*
United Kingdom  115391.13
Netherlands     5430.7295
EIRE    3797.973
Germany 3223.3242
France  3012.7568
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis2/Job4/part*|head -n 10
12346   77183.59
15749   7837.5
12357   6207.67
12688   4873.81
12752   4366.78
18251   4314.7197
12536   4161.06
12378   4008.62
15195   3861.0
12435   3850.9
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis2/Job5/part*|head -n 10
16446   168469.6
12346   77183.59
15098   38970.0
17450   31698.16
12415   22775.93
18102   22206.0
15749   21535.9
14646   20277.92
12931   18841.48
14156   16774.72
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis2/Job6/part*|head -n 10
16446   84236.25
12346   77183.59
15749   14844.767
15098   13305.5
12357   6207.67
12415   5948.311
12590   4932.13
12688   4873.81
12752   4366.78
18102   4327.6216
kali@kali:~$ 

#**

***** note that for jobs 4, 5, 6 the viewed results are limited to top 10 outputs to avoid printing all 4339 results ****
*/
