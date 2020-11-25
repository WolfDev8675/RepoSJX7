/*Analysis 4: 
In india find out the states where the death is highest */

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
preset4 = FOREACH data_collect GENERATE Country,Province,Deaths; --pre assemble
preset4fx = FILTER preset4 BY (Country == 'India' AND Province != ''); -- filtered 
preset4Grp = GROUP preset4fx BY Province; --group 
analysis4uo = FOREACH preset4Grp GENERATE group as (Province:chararray), SUM(preset4fx.Deaths) as (DCount:int); --unordered result 
analysis4 = ORDER analysis4uo BY DCount DESC; -- final result 
STORE analysis4 INTO '/home/kali/Hadoop/Results/pig_results3/analysis4/' USING PigStorage();  -- storage 


/* Results obtained 
kali@kali:~$ cat /home/kali/Hadoop/Results/pig_results3/analysis4/* 
Maharashtra     1757974
Tamil Nadu      457240
Delhi   388327
Karnataka       323412
Gujarat 259068
Uttar Pradesh   222519
Andhra Pradesh  213593
West Bengal     208712
Madhya Pradesh  106583
Punjab  87612
Rajasthan       78890
Telangana       59913
Haryana 51992
Jammu and Kashmir       45336
Bihar   38665
Odisha  27561
Jharkhand       21734
Assam   17956
Chhattisgarh    17382
Kerala  16691
Uttarakhand     16450
Puducherry      13232
Goa     10614
Tripura 6415
Chandigarh      3483
Himachal Pradesh        3007
Andaman and Nicobar Islands     2009
Manipur 1531
Ladakh  1514
Meghalaya       862
Nagaland        543
Arunachal Pradesh       451
Sikkim  373
Dadra and Nagar Haveli and Daman and Diu        143
Mizoram 0
Unknown 0
Dadar Nagar Haveli      0
kali@kali:~$ 
*/
