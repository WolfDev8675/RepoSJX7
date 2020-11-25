/*Analysis 6: 
Find out the avg confirmed avg death avg active case month wise for India for state WestBengal*/

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
preset61 = FOREACH data_collect GENERATE LastUpdate,Country,Province,Confirmed,Deaths,Active; -- assemble 1
preset61fx = FILTER preset61 BY (Country == 'India' AND Province == 'West Bengal'); -- filtered
preset62 = FOREACH preset61fx GENERATE CONCAT((chararray)GetMonth(LastUpdate),'-',(chararray)GetYear(LastUpdate)) as (mmyyyy:chararray),Confirmed,Deaths,Active; -- final assemble
preset62Gpr = GROUP preset62 BY mmyyyy;  --month-year group 
analysis6 = FOREACH preset62Gpr GENERATE group,AVG(preset62.Confirmed),AVG(preset62.Deaths),AVG(preset62.Active);  -- calculate 
STORE analysis6 INTO '/home/kali/Hadoop/Results/pig_results3/analysis6/' USING PigStorage();  -- storage 


/* Results obtained 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results3/analysis6/* 
6-2020  13323.25        536.2   5242.15
7-2020  37955.41935483871       1035.0  12953.129032258064
8-2020  114114.96774193548      2372.8064516129034      25670.677419354837
9-2020  196917.5        3847.75 24015.083333333332
kali@kali:~$ 
*/
