/*Analysis 4: 
Find out the Avg confirmed Avg death Avg active case month wise for India*/

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
preset51 = FOREACH data_collect GENERATE LastUpdate,Country,Province,Confirmed,Deaths,Active; -- assemble 1
preset51fx = FILTER preset51 BY (Country == 'India' AND Province != ''); -- filtered
preset52 = FOREACH preset51fx GENERATE CONCAT((chararray)GetMonth(LastUpdate),'-',(chararray)GetYear(LastUpdate)) as (mmyyyy:chararray),Confirmed,Deaths,Active;
preset52Gpr = GROUP preset52 BY mmyyyy;
analysis5 = FOREACH preset52Gpr GENERATE group,AVG(preset52.Confirmed),AVG(preset52.Deaths),AVG(preset52.Active);
STORE analysis5 INTO '/home/kali/Hadoop/Results/pig_results3/analysis5/' USING PigStorage();  -- storage 


/* Results obtained 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results3/analysis5/* 
6-2020  11390.589707927676      352.105702364395        4755.609179415856
7-2020  28480.81834532374       712.8381294964029       9836.422661870503
8-2020  74345.86924493554       1430.3637200736648      18982.435543278083
9-2020  133410.62976190477      2217.347619047619       26609.489285714284
kali@kali:~$ 
*/
