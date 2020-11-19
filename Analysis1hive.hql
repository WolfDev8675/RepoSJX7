 -- Analysis 1: 
-- Find the country with rising cases 

-- start of codes
-- one time jobs 
-- **## Please avoid lines here on forward if sars_covid19db is available in 'show databases' command and contains data                   ##**
 create database sars_covid19db;
 use sars_covid19db;
 create table data_raw_headless 
 (SNo int,ObservationDate string,Province string,Country string,LastUpdate string,Confirmed int,Deaths int ,Recovered int) 
 row format delimited fields terminated by ',' lines terminated by '\n' tblproperties("skip.header.line.count"="1");
 load data inpath 'hdfs://localhost:9000/user/hive/warehouse/covid_19_data.csv' into table data_raw_headless;
