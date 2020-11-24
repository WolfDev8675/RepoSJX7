-- Cleaning of the data for use in Spark operations 

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

-- date corrected 
create table data_collect_s (sno int,lastupdate string,province string,country string,confirmed int,deaths int,recovered int,active int);
insert into data_collect_s select sno,from_unixtime(unix_timestamp(lastupdate,'yyyy-MM-dd HH:mm:ss')),province,country,confirmed,deaths,recovered,(confirmed-(deaths+recovered)) from data_collect 
where confirmed!=(deaths+recovered);

-- directing storage 
insert overwrite directory '/assign3/clean_data' row format delimited fields terminated by '\t' lines terminated by '\n' select * from data_collect_s;

-- cleaned data stored in hdfs://localhost:9000/assign3/clean_data/* 
