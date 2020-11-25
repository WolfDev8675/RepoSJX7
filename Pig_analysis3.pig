/*Analysis 3: 
In India show the cases state wise no of confirmed and active*/

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
preset3 = FOREACH data_collect GENERATE Country,Province,Confirmed,Active; --pre assemble
preset3fx = FILTER preset3 BY (Country == 'India' AND Province != ''); -- filtered 
preset3Grp = GROUP preset3fx BY Province; --group 
analysis3uo = FOREACH preset3Grp GENERATE group as (Province:chararray), SUM(preset3fx.Confirmed),SUM(preset3fx.Active); --unordered result 
analysis3 = ORDER analysis3uo BY Province; -- final result 
STORE analysis3 INTO '/home/kali/Hadoop/Results/pig_results3/analysis3/' USING PigStorage();  -- storage 


/* Results obtained 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results3/analysis3/* 
Andaman and Nicobar Islands     154034  34108
Andhra Pradesh  23442531        5775776
Arunachal Pradesh       246208  80115
Assam   6313710 1494730
Bihar   7595943 1390568
Chandigarh      273649  96698
Chhattisgarh    2153566 941480
Dadar Nagar Haveli      22      20
Dadra and Nagar Haveli and Daman and Diu        139392  27596
Delhi   14492502        2037142
Goa     1023301 263582
Gujarat 7003453 1289055
Haryana 4541196 918482
Himachal Pradesh        404818  134216
Jammu and Kashmir       2610509 799996
Jharkhand       2325059 718928
Karnataka       19353593        5914002
Kerala  4309551 1391503
Ladakh  187927  54691
Madhya Pradesh  4325668 986470
Maharashtra     53940053        15812141
Manipur 388742  125146
Meghalaya       141777  72760
Mizoram 65657   29196
Nagaland        245013  91432
Odisha  5944304 1463227
Puducherry      759708  234629
Punjab  3186784 887965
Rajasthan       5396381 1073416
Sikkim  94143   31845
Tamil Nadu      28118938        4851779
Telangana       7909147 1913481
Tripura 771904  267414
Unknown 233513  233513
Uttar Pradesh   13579785        3604910
Uttarakhand     1285899 403726
West Bengal     9706667 1878543
kali@kali:~$ 
*/
