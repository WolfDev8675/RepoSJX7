/*Analysis 3: 
Select any year for which data is available: 
--> For the selected year, create a table that contains data only for those stocks that have an average total traded quntity of 3 lakhs or more per day.
--> Print out the first 25 entries of the table and submit.
--> From above output, select any 10 stocks from IT ('HCLTECH', 'NIITTECH', 'TATAELXSI','TCS', 'INFY', 'WIPRO', 'DATAMATICS','TECHM','MINDTREE' and 'OFSS')
       and create a table combining their data. Find out the Pearsons Correlation Coeffecient for every pair of stocks you have selected above. 
--> Final output should be in decreasing order of the coeffecient */

-- start of code 

--raw data load with defined schema 
data_raw= LOAD '/home/kali/Hadoop/Local_Datasets/FINAL_FROM_DF.csv' USING PigStorage(',') as (SYMBOL:chararray,SERIES:chararray,OPEN:float,HIGH:float,LOW:float,CLOSE:float,LAST:float,PREVCLOSE:float,TOTTRDQTY:int,TOTTRDVAL:float,TIMESTAMPS:Datetime,TOTALTRADES:int,ISIN:chararray);
data_collect = FILTER data_raw BY (OPEN>=0); --cleaning with condition (collect = headless)
rawGrp = GROUP data_raw ALL; --checker group 
cltGrp = GROUP data_collect ALL; --checker group 
ctrrw = FOREACH rawGrp GENERATE COUNT(data_raw);  -- counter value (846405)
ctrclt = FOREACH cltGrp GENERATE COUNT(data_collect); -- counter value (846404)
dump ctrrw --trigger calculation
dump ctrclt --trigger calculation

--no visible debris ... collect-> headless
-- 
--

--analysis job
-- selected year 2017 
precoll3 = FILTER data_collect BY GetYear(TIMESTAMPS)==2017;  -- filter by selected year 
anlysjob3a = FILTER precoll3 BY TOTTRDVAL>=300000;   -- filter by specified criteria 
f25_anlysjob3a = LIMIT anlysjob3a 25;  --  test variable to get first 25 entries in 'anlysjob3a' 
STORE f25_anlysjob3a INTO '/home/kali/Hadoop/Results/pig_results2/analysis3/a/' USING PigStorage();  -- store cycle 1
dump f25_anlysjob3a;  -- dumped to release values 
--  ** filtration by 10 specified IT labels in SYMBOL column
anlysjob3b = FILTER anlysjob3a BY SYMBOL IN ('HCLTECH', 'NIITTECH', 'TATAELXSI','TCS', 'INFY', 'WIPRO', 'DATAMATICS','TECHM','MINDTREE','OFSS');
it3left = FOREACH anlysjob3b GENERATE SYMBOL,CLOSE; -- left joiner
it3right = FOREACH anlysjob3b GENERATE SYMBOL,CLOSE; -- right joiner
crosscoll3 = FILTER (CROSS it3left,it3right) BY  it3left.SYMBOL < it3right.SYMBOL;  --cross collection with filtration by inequal symbol criteria 
-- arrangement as per requirement 
arranged = FOREACH crosscoll3 GENERATE it3left.SYMBOL as (sym1:chararray),it3right.SYMBOL as (sym2:chararray),it3left.CLOSE as (val1:float),it3right.CLOSE as (val2:float),
it3left.CLOSE*it3left.CLOSE as (val1p2:float),it3right.CLOSE*it3right.CLOSE as (val2p2:float),it3left.CLOSE*it3right.CLOSE as (val12:float);
arng_grp = GROUP arranged BY (sym1,sym2);  -- grouping 
-- final solution 
anlysjob3_ = FOREACH arng_grp GENERATE group,(AVG(arranged.val12)-(AVG(arranged.val1)*AVG(arranged.val2)))/(SQRT(SUM(arranged.val1p2)/COUNT(arranged.val1p2) - AVG(arranged.val1)*AVG(arranged.val1))*SQRT(SUM(arranged.val2p2)/COUNT(arranged.val2p2) - AVG(arranged.val2)*AVG(arranged.val2))) as (rho:float);   
anlysjob3 = ORDER anlysjob3_ BY rho;
STORE anlysjob3 INTO '/home/kali/Hadoop/Results/pig_results2/analysis3/b/' USING PigStorage();  -- store cycle 2
