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
create table preset31 as select * from data_raw_headless where year(from_unixtime(unix_timestamp(timestamps,'yyyy-MM-dd')))== 2017;
create table anlysjob3a as select * from preset31 where tottrdval>=300000;
-- first 25 entries
select * from anlysjob3a limit 25;
--10 IT stocks 
create table anlysjob3b as select * from anlysjob3a 
where symbol =='HCLTECH' OR symbol == 'NIITTECH' OR symbol == 'TATAELXSI' OR symbol == 'TCS' OR symbol == 'INFY' OR symbol == 'WIPRO'
OR symbol == 'DATAMATICS' OR symbol == 'TECHM' OR symbol == 'MINDTREE' OR symbol == 'OFSS';
create table it3left as select symbol,close from anlysjob3b;
create table it3right as select symbol,close from anlysjob3b;
create table crosscoll3 (sym1 string,sym2 string,val1 float,val2 float);
insert into crosscoll3 select it3left.symbol, it3right.symbol, it3left.close,it3right.close from it3left cross join it3right 
where it3left.symbol < it3right.symbol;
create table anlysjob3(sym1 string,sym2 string,rho float);
insert into anlysjob3 select sym1,sym2,(avg(val1*val2)-(avg(val1)*avg(val2)))/(stddev_pop(val1)*stddev_pop(val2)) as rho from crosscoll3 
group by sym1,sym2 order by rho;


-- obtained result 
--
