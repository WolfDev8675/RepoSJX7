
-- Analysis 1: 
--  Use the given csv file as input data and implement following transformations: 
-- Filter Rows on specified criteria "Symbol equals GEOMETRIC" 
-- Select specific columns from those available: SYMBOL, OPEN, HIGH, LOW and CLOSE which meets above criteria 
-- Generate count of the number of rows from above result

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
