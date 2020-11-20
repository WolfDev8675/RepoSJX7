 -- Analysis 1: 
-- Find the country with rising cases 

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
create table preset1 (country string, t_rec int, t_act int);
insert into preset1 select country, sum(recovered), sum(active) from data_collect group by country;
-- results final 
create table analysis1 as select country from preset1 where t_act>t_rec;
-- end of codes

-- Results obtained 
--** HIVE shell
--
--hive> select * from analysis1 limit 10 ;
--OK
-- Azerbaijan
--Angola
--Aruba
--Bahamas
--Belgium
--Belize
--Bolivia
--Botswana
--Burma
--Cape Verde
--Time taken: 0.243 seconds, Fetched: 10 row(s)
--hive> 

-- *** results limited to 10 results to limit cluttering screen from 68 countries***
