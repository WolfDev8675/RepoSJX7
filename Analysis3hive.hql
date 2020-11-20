-- Analysis 3: 
-- In India show the cases state wise no of confirmed and active 

-- start of codes
-- one time jobs 
-- **## Please avoid lines here on forward if sars_covid19db is available in 'show databases' command and contains data                   ##**
create database sars_covid19db;
use sars_covid19db;
--create dataset
create table data_raw_headless 
(SNo int,ObservationDate string,Province string,Country string,LastUpdate string,Confirmed int,Deaths int ,Recovered int) 
row format delimited fields terminated by ',' lines terminated by '\n' tblproperties("skip.header.line.count"="1");
load data inpath 'hdfs://localhost:9000/user/hive/warehouse/covid_19_data.csv' into table data_raw_headless;
-- find number of datapoints
select count(SNo) from data_raw_headless where country!='';
-- value 116805
-- generating usable data
create table data_collect (sno int,lastupdate string,province string,country string,confirmed int,deaths int,recovered int,active int);
insert into data_collect select sno,lastupdate,province,country,confirmed,deaths,recovered,(confirmed-(deaths+recovered)) data_raw_headless 
where confirmed!=(deaths+recovered);
-- finding number of datapoints
select count(sno) from data_collect where country !='';
-- value 107749
-- cleaned data in data_collect

-- analysis jobs 
-- creating preset collection
create table preset3 as select country,province,confirmed,active from data_collect where country=='India' AND province!='';
create table analysis3 as select province,sum(confirmed),sum(active) from preset3 group by province order by province;
--end of codes

-- Results obtained 
--** HIVE shell
--
--hive> select * from analysis3;
OK
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
Time taken: 0.271 seconds, Fetched: 37 row(s)
hive> 

