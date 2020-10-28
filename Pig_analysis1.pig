/*Analysis 1: 
Revenue Aggregate by country for top 5 countries */

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
kvp_asgn1 = FOREACH data_cleaned GENERATE Country as (Country:chararray), UnitPrice*Quantity as (TotalCost:float); -- kv map for generating aggregate 
resGrp = GROUP kvp_asgn1 BY Country; -- group by country 
--illustrate -- check type for next line 
resFinal = FOREACH resGrp GENERATE group as (Country:chararray),SUM(kvp_asgn1.TotalCost) as (Revenue:float); --group sum of revenues
ordered_res = ORDER resFinal BY Revenue DESC; -- descending order 
ordered_res5= LIMIT ordered_res 5; -- top 5 countries -> revenue aggregate
STORE ordered_res5 INTO '/home/kali/Hadoop/Results/pig_results/analysis1/' USING PigStorage();

/* 
** Results obtained 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis1/part*
United Kingdom  7308391.5
Netherlands     285446.34
EIRE    265545.9
Germany 228867.14
France  209024.05
kali@kali:~$ 
*.



