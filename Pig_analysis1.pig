/*Analysis 1: 
Find the country with rising cases */

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
data_collect= FOREACH data_cleaned GENERATE SNo,LastUpdate,Province,Country,Confirmed,Deaths,Recovered,(Confirmed-(Deaths+Recovered)) as (Active:int);
-- cleaned of debris in data 

--analysis jobs
preset1= FOREACH data_collect GENERATE Country,Recovered,Active;
preset1Grp = GROUP preset1 BY Country;
analysis1coll = FOREACH preset1Grp GENERATE group as (Country:chararray),SUM(preset1.Recovered) as (T_rec:int),SUM(preset1.Active) as (T_act:int); --calculated
analysis1fx= FILTER analysis1coll BY (T_rec < T_act); -- filterd but unordered 
analysis1uo= FOREACH analysis1UO GENERATE Country;  --collect answers unordered
analysis1 = ORDER analysis1uo BY Country;  -- final result
STORE analysis1 INTO '/home/kali/Hadoop/Results/pig_results3/analysis1/' USING PigStorage();  -- storage 


/* Results obtained 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results3/analysis1/* | head -n 10
 Azerbaijan
Angola
Aruba
Bahamas
Belgium
Belize
Bolivia
Botswana
Burma
Cape Verde
kali@kali:~$ 
 */
