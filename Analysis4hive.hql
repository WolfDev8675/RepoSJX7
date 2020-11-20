-- Analysis 4: 
-- In india find out the states where the death is highest 

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
create table preset4 as select country,province,deaths from data_collect where country=='India' AND province!='';
create table analysis4 as select province,sum(deaths) as d_count from preset4 group by province order by d_count;
--end of codes;

-- Results obtained 
--** HIVE shell
--
--hive> select * from analysis4;
--OK
--Maharashtra     1757974
--Tamil Nadu      457240
--Delhi   388327
--Karnataka       323412
--Gujarat 259068
--Uttar Pradesh   222519
--Andhra Pradesh  213593
--West Bengal     208712
--Madhya Pradesh  106583
--Punjab  87612
--Rajasthan       78890
--Telangana       59913
--Haryana 51992
--Jammu and Kashmir       45336
--Bihar   38665
--Odisha  27561
--Jharkhand       21734
--Assam   17956
--Chhattisgarh    17382
--Kerala  16691
--Uttarakhand     16450
--Puducherry      13232
--Goa     10614
--Tripura 6415
--Chandigarh      3483
--Himachal Pradesh        3007
--Andaman and Nicobar Islands     2009
--Manipur 1531
--Ladakh  1514
--Meghalaya       862
--Nagaland        543
--Arunachal Pradesh       451
--Sikkim  373
--Dadra and Nagar Haveli and Daman and Diu        143
--Dadar Nagar Haveli      0
--Mizoram 0
--Unknown 0
--Time taken: 0.22 seconds, Fetched: 37 row(s)
--hive> 
--
--*****
