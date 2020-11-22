/*Analysis 2: 
 Calculation of various statistical quantities and decision making:
 Only lines with value "EQ" in the "series" column should be processed. 
 As the first stage, filter out all the lines that do not fulfil this criteria. 
 For every stock(with value "EQ" in the "series"), for every year, 
 calculate the statistical parameters(Minimum, Maximum, Mean and Standard Deviation) 
 and store the generated information in properly designated tables. */

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
pre_coll2 = FILTER data_collect BY (SERIES=='EQ');   -- prefilter with SERIES equals 'EQ'
finalcoll2 = FOREACH pre_coll2 GENERATE SYMBOL,GetYear(TIMESTAMPS) as (YEAR:int),CLOSE as (W_field:float), CLOSE*CLOSE as (W_field2:float);  -- collection of required fields 
calc_grp = GROUP finalcoll2 BY (SYMBOL,YEAR);  -- calculation group
-- finalizing required calculations 
anlysjob2_ = FOREACH calc_grp GENERATE group as gp,MIN(finalcoll2.W_field),MAX(finalcoll2.W_field),AVG(finalcoll2.W_field),SQRT(SUM(finalcoll2.W_field2)/COUNT(finalcoll2.W_field2) - AVG(finalcoll2.W_field)*AVG(finalcoll2.W_field));
anlysjob2 = ORDER anlysjob2_ BY SYMBOL;  -- final order
 
 --Storage 
 STORE anlysjob2 INTO '/home/kali/Hadoop/Results/pig_results2/analysis2/' USING PigStorage();
 --

/*
Solution stored limited to 10 results 

kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results2/analysis2/part* |head -n 10
(20MICRONS,2016)        25.45   43.15   32.56518223411158       4.449799144115362
(20MICRONS,2017)        33.7    62.7    41.634072642172534      6.59098207014905
(3IINFOTECH,2016)       3.8     6.8     5.012348183736145       0.7338402417837622
(3IINFOTECH,2017)       3.7     8.0     4.663104832172394       0.7633750476806549
(3MINDIA,2016)  9521.5  14939.55        12146.576930984313      1292.3010897787285
(3MINDIA,2017)  10789.9 19366.4 13443.495959866432      1687.908552108419
(5PAISA,2017)   187.3   388.75  283.72618902297245      67.2148122582015
(63MOONS,2017)  54.9    159.65  84.53957428627825       23.649053295859137
(8KMILES,2016)  591.3   2483.7  1646.2582968275556      541.7588940911268
(8KMILES,2017)  369.5   987.9   613.1727826518397       138.32717721849752
kali@kali:~$ 

*/
