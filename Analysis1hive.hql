-- Analysis 1: 
--  Use the given csv file as input data and implement following transformations: 
-- a. Filter Rows on specified criteria "Symbol equals GEOMETRIC" 
-- b. Select specific columns from those available: SYMBOL, OPEN, HIGH, LOW and CLOSE which meets above criteria 
-- c. Generate count of the number of rows from above result

-- start of codes
-- one time jobs 
-- **## Please avoid lines here on forward if nsestocksdb is available in 'show databases' command and contains data                   ##**
-- ** and jump to the section of analysis **
create database nsestocksdb;
use nsestocksdb;
--create dataset
create table data_raw_headless 
(SYMBOL string,SERIES string,OPEN float,HIGH float,LOW float,CLOSE float,LAST float,PREVCLOSE float,
TOTTRDQTY int,TOTTRDVAL float,TIMESTAMPS string,TOTALTRADES int,ISIN string) 
row format delimited fields terminated by ',' lines terminated by '\n' tblproperties("skip.header.line.count"="1");
load data inpath 'hdfs://localhost:9000/user/hive/warehouse/FINAL_FROM_DF.csv' into table data_raw_headless;
-- find number of datapoints
select count(*) from data_raw_headless where isin!='';
-- result 846404

-- analysis jobs 
--
create table anlysjob1a as select * from data_raw_headless where symbol=='GEOMETRIC';
create table anlysjob1b as select symbol,open,high,low,close from anlysjob1a;
select count(*) from anlysjob1b 


-- obtained result 
--hive> select count(*) from anlysjob1b ;--
--OK
--295
--Time taken: 0.441 seconds, Fetched: 1 row(s)
--hive> 
