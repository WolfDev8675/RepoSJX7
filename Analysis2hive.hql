-- Analysis 2: 
--   Calculation of various statistical quantities and decision making: 
-- Only lines with value "EQ" in the "series" column should be processed. 
-- As the first stage, filter out all the lines that do not fulfil this criteria. 
-- For every stock(with value "EQ" in the "series"), for every year, calculate the statistical parameters
-- (Minimum, Maximum, Mean and Standard Deviation) and store the generated information in properly designated tables.

-- start of codes
-- one time jobs 
-- **## Please avoid lines here on forward if sars_covid19db is available in 'show databases' command and contains data                   ##**
create database nsestocksdb;
use sars_nsestocksdb;
--create dataset
create table data_raw_headless 
(SYMBOL string,SERIES string,OPEN float,HIGH float,LOW float,CLOSE float,LAST float,PREVCLOSE float,
TOTTRDQTY int,TOTTRDVAL float,TIMESTAMPs string,TOTALTRADES int,ISIN string) 
row format delimited fields terminated by ',' lines terminated by '\n' tblproperties("skip.header.line.count"="1");
load data inpath 'hdfs://localhost:9000/user/hive/warehouse/FINAL_FROM_DF.csv' into table data_raw_headless;
-- find number of datapoints
select count(*) from data_raw_headless where isin!='';
-- result 846404

-- analysis jobs 
--
create table pre_coll2 as select * from data_raw_headless where series=='EQ';
create table spc_coll2 (symbol string,timeval bigint,w_field float);
insert into spc_coll2 select symbol,unix_timestamp(timestamps,'yyyy-MM-dd'),close from pre_coll2;
create table finalcoll2 as select symbol,year(from_unixtime(timeval)) as year,w_field from spc_coll2;
