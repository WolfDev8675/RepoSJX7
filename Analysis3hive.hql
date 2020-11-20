-- Analysis 3: 
--  Select any year for which data is available: 
-- For the selected year, create a table that contains data only for those stocks that have an average total traded quntity of 3 lakhs or more per day.
-- Print out the first 25 entries of the table and submit.
-- From above output, select any 10 stocks from IT ('HCLTECH', 'NIITTECH', 'TATAELXSI','TCS', 'INFY', 'WIPRO', 'DATAMATICS','TECHM','MINDTREE' and 'OFSS')
-- and create a table combining their data. Find out the Pearsons Correlation Coeffecient for every pair of stocks you have selected above. 
-- Final output should be in decreasing order of the coeffecient

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
create table preset21 as select * from data_raw_headless where year(from_unixtime(unix_timestamp(timestamps,'yyyy-MM-dd')))== 2017;



-- obtained result 
--
