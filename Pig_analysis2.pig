/*Analysis 2: 
Find the active case of top 5 country */

-- start of code 

--raw data load with defined schema 
data_raw= LOAD '/home/kali/Hadoop/Local_Datasets/covid_19_data.csv' USING PigStorage(',') as (SNo:int,ObservationDate:datetime,Province:chararray,Country:chararray,LastUpdate:datetime,Confirmed:int,Deaths:int ,Recovered:int);
data_cleaned = FILTER data_raw BY (Confirmed != (Deaths+Recovered)); --cleaning with condition 
ctrRawG= GROUP data_raw ALL;  -- grouping raw to count 
ctrClnG= GROUP data_cleaned ALL; -- grouping cleaned to count 
ctrRaw= FOREACH ctrRawG GENERATE COUNT(data_raw.SNo);  --generating count raw 
ctrCln= FOREACH ctrClnG GENERATE COUNT(data_cleaned.SNo); -- generating count cleaned 
-- dumping to trigger results' calculation
dump ctrRaw --value :: (116805)
dump ctrCln --value :: (107749)
-- collect final clean collection 
data_collect= FOREACH data_cleaned GENERATE SNo,LastUpdate,Province,Country,Confirmed,Deaths,Recovered,(Confirmed-(Deaths+Recovered)) as (Active:int);
-- cleaned of debris in data 

--analysis jobs
preset2= FOREACH data_collect GENERATE Country,Active; -- primary assemble
preset2Grp = GROUP preset2 BY Country;    -- grouping
analysis2uo = FOREACH preset2Grp GENERATE group as (Country:chararray),SUM(preset2.Active) as (T_act:int); -- unordered results
analysis2fx = ORDER analysis2uo BY T_act DESC; -- final ordered result 
analysis2 = LIMIT analysis2fx 5; -- final result 
STORE analysis2 INTO '/home/kali/Hadoop/Results/pig_results3/analysis2/' USING PigStorage();  -- storage 


/* Results obtained 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results3/analysis2/* 
US      361485183
Brazil  60868651
India   60501744
UK      40370420
Russia  29711685
kali@kali:~$ 
*/
