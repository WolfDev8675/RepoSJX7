-- Analysis 6: 
-- Find out the avg confirmed avg death avg active case month wise for India for state WestBengal

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
-- creating preset collection leaving out reports where no province is specified.
create table preset61 (timeval bigint,country string,confirmed int,deaths int,active int);
insert into preset61 select (unix_timestamp(lastupdate,'yyyy-MM-dd HH:mm:ss')),country,confirmed,deaths,active from data_collect where country=='India' AND province=='West Bengal';
create table preset62(mmyyyy string,confirmed int,deaths int,active int);
insert into preset62 select concat(cast(month(from_unixtime(timeval)) as string),'-',cast(year(from_unixtime(timeval)) as string)),confirmed,deaths,active from preset61;
-- results final 
create table analysis6 as select mmyyyy,avg(confirmed),avg(deaths),avg(active) from preset62 group by mmyyyy;
--end of codes

-- Results obtained 
--** HIVE shell
--
--hive> select * from analysis6;
--OK
--6-2020  13323.25        536.2   5242.15
--7-2020  37955.41935483871       1035.0  12953.129032258064
--8-2020  114114.96774193548      2372.8064516129034      25670.677419354837
--9-2020  196917.5        3847.75 24015.083333333332
--Time taken: 0.162 seconds, Fetched: 4 row(s)
--hive> 
--
--****
