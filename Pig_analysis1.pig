/*Analysis 1: 
 Use the given csv file as input data and implement following transformations: 
 a. Filter Rows on specified criteria "Symbol equals GEOMETRIC" 
 b. Select specific columns from those available: SYMBOL, OPEN, HIGH, LOW and CLOSE which meets above criteria 
 c. Generate count of the number of rows from above result */

-- start of code 

--raw data load with defined schema 
data_raw= LOAD '/home/kali/Hadoop/Local_Datasets/FINAL_FROM_DF.csv' USING PigStorage(',') as (SYMBOL:chararray,SERIES:chararray,OPEN:float,HIGH:float,LOW:float,CLOSE:float,LAST:float,PREVCLOSE:float,TOTTRDQTY:int,TOTTRDVAL:float,TIMESTAMPS:Datetime,TOTALTRADES:int,ISIN:chararray);
data_collect = FILTER data_raw BY (OPEN>=0); --cleaning with condition (collect = headless)
rawGrp = GROUP data_raw ALL; --checker group 
cltGrp = GROUP data_collect ALL; --checker group 
ctrrw = FOREACH rawGrp GENERATE COUNT(data_raw);  -- counter value (846405)
ctrclt = FOREACH clnGrp GENERATE COUNT(data_collect); -- counter value (846404)
dump ctrrw --trigger calculation
dump ctrclt --trigger calculation

--no visible debris ... collect-> headless
-- 
--

--analysis job
anlysjob1a = FILTER data_collect BY (SYMBOL=='GEOMETRIC');  -- option -a
anlysjob1b = FOREACH anlysjob1a GENERATE SYMBOL,OPEN,HIGH,LOW,CLOSE ;  --option -b
soln_grp = GROUP anlysjob1b ALL; -- group counter
anlysjob1c = FOREACH soln_grp GENERATE COUNT(anlysjob1b) ;

-- Storage and dump 
STORE anlysjob1c INTO '/home/kali/Hadoop/Results/pig_results2/analysis1/' USING PigStorage();
dump anlysjob1c;

/*
dump value: 295

stored 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results2/analysis1/part*
295
kali@kali:~$ 

*/
