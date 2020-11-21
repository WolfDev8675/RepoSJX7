-- Analysis 2: 
--   Calculation of various statistical quantities and decision making: 
-- Only lines with value "EQ" in the "series" column should be processed. 
-- As the first stage, filter out all the lines that do not fulfil this criteria. 
-- For every stock(with value "EQ" in the "series"), for every year, calculate the statistical parameters
-- (Minimum, Maximum, Mean and Standard Deviation) and store the generated information in properly designated tables.

-- start of codes
-- one time jobs 
-- **## Please avoid lines here on forward if nsestocksdb is available in 'show databases' command and contains data                   ##**
create database nsestocksdb;
use nsestocksdb;
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
create table finalcoll2 (symbol string,year int,w_field float);
insert into finalcoll2 select symbol,year(from_unixtime(timeval)) as year,w_field from spc_coll2;
create table anlysjob2 as select symbol,year,min(w_field),max(w_field),avg(w_field),stddev_pop(w_field) from finalcoll2 group by symbol,year order by symbol;

-- obtained result 
--hive> select * from  anlysjob2 limit 10;
--OK
--20MICRONS       2016    25.45   43.15   32.56518223411158       4.449799086240495
--20MICRONS       2017    33.7    62.7    41.634072642172534      6.590982144829505
--3IINFOTECH      2016    3.8     6.8     5.012348183736145       0.7338403196788177
--3IINFOTECH      2017    3.7     8.0     4.663104832172394       0.763375120711009
--3MINDIA 2016    9521.5  14939.55        12146.576930984313      1292.3010060900851
--3MINDIA 2017    10789.9 19366.4 13443.495959866432      1687.908570027977
--5PAISA  2017    187.3   388.75  283.72618902297245      67.21481238608698
--63MOONS 2017    54.9    159.65  84.53957428627825       23.64905316934828
--8KMILES 2016    591.3   2483.7  1646.2582968275556      541.7589068616428
--8KMILES 2017    369.5   987.9   613.1727826518397       138.32717290909883
--Time taken: 0.172 seconds, Fetched: 10 row(s)
--hive> 

--****  result has 3345 elements result restricted to 10 elements
