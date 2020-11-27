/* Analysis 6:
Top 20 Items sold by frequency*/
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
-- Job: Top 20 items sold by frequency 
kv_asses6 = FOREACH data_cleaned GENERATE CONCAT(StockCode,'->',Description) as (Item:chararray),(Quantity) as (Quantity:int);  --- kv group item to quantity
kv_asses6grp = GROUP kv_asses6 BY Item; -- grouping by item 
analysis6res = FOREACH kv_asses6grp GENERATE group as (Items:chararray),SUM(kv_asses6.Quantity) as (Frequency:int);
orderedRes = ORDER analysis6res BY Frequency DESC;    -- ordering 
result6 = LIMIT orderedRes 20; -- limiting
STORE result6 INTO '/home/kali/Hadoop/Results/pig_results/analysis6/' USING PigStorage();   -- storing 

-- end of code 

/*
** Results Obtained 
#** 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results/analysis6/part*
23843->"PAPER CRAFT , LITTLE BIRDIE"    80995
23166->MEDIUM CERAMIC TOP STORAGE JAR   77916
84077->WORLD WAR 2 GLIDERS ASSTD DESIGNS        54415
85099B->JUMBO BAG RED RETROSPOT 46181
85123A->WHITE HANGING HEART T-LIGHT HOLDER      36725
84879->ASSORTED COLOUR BIRD ORNAMENT    35362
21212->PACK OF 72 RETROSPOT CAKE CASES  33693
22197->POPCORN HOLDER   30931
23084->RABBIT NIGHT LIGHT       27202
22492->MINI PAINT SET VINTAGE   26076
22616->PACK OF 12 LONDON TISSUES        25345
21977->PACK OF 60 PINK PAISLEY CAKE CASES       24264
17003->BROCADE RING PURSE       22963
22178->VICTORIAN GLASS HANGING T-LIGHT  22433
15036->ASSORTED COLOURS SILK FAN        21876
21915->RED  HARMONICA IN BOX    20975
22386->JUMBO BAG PINK POLKADOT  20165
22197->SMALL POPCORN HOLDER     18252
20725->LUNCH BAG RED RETROSPOT  17697
84991->60 TEATIME FAIRY CAKE CASES      17689
kali@kali:~$
#**

*/
