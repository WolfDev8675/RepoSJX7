-- Analysis 5: 
-- Find out the Avg confirmed Avg death Avg active case month wise for India 

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
-- analysis jobs 
-- creating preset collection
create table preset51 (timeval bigint,country string,confirmed int,deaths int,active int);
insert into preset51 select (unix_timestamp(lastupdate,'yyyy-MM-dd HH:mm:ss')),country,confirmed,deaths,active from data_collect where country=='India' AND province!='';
create table preset52(mmyyyy string,confirmed int,deaths int,active int);
insert into preset52 select concat(cast(month(from_unixtime(timeval)) as string),'-',cast(year(from_unixtime(timeval)) as string)),confirmed,deaths,active from preset51;
create table analysis5 as select mmyyyy,avg(confirmed),avg(deaths),avg(active) from preset52 group by mmyyyy;
-- results final ;
hive> select * from analysis5;
OK
6-2020  11390.589707927676      352.105702364395        4755.609179415856
7-2020  28480.81834532374       712.8381294964029       9836.422661870503
8-2020  74345.86924493554       1430.3637200736648      18982.435543278083
9-2020  133410.62976190477      2217.347619047619       26609.489285714284
Time taken: 0.183 seconds, Fetched: 4 row(s)
hive> 
