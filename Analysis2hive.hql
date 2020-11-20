-- Analysis 2: 
-- Find the active case of top 5 country

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
create table preset2 (country string,t_act int);
insert into preset2 select country,sum(active) as t_act from data_collect group by country order by t_act desc; 
-- final result 
create table analysis2 as select * from preset2 order by t_act desc limit 5;
--end of codes

-- Results obtained 
--** HIVE shell
--
--hive> select * from analysis2 ;
--OK
--US      361485183
--Brazil  60868651
--India   60501744
--UK      40370420
--Russia  29711685
--Time taken: 0.222 seconds, Fetched: 5 row(s)
--hive> 
-- *****
