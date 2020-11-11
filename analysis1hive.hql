-- Analysis 1: 
-- Revenue Aggregate by country for top 5 countries 

-- start of codes
-- one time jobs 
-- **## Please avoid lines here on forward if retaildb is available in 'show databases' command and contains data                   ##**
-- **## if avoiding these lines till line 23 directly jump to codes in analysis section of the code which next to this section      ##**
create database RetailDB;
use RetailDB;
-- table creation 
create table data_raw_headless (InvoiceNo string,StockCode string,Description string,Quantity int,InvoiceDate string,UnitPrice float,CustomerID string,Country string) row format delimited fields terminated by '\t' lines terminated by '\n' tblproperties("skip.header.line.count"="1");
load data inpath 'hdfs://localhost:9000/user/hive/warehouse/OnlineRetail.txt' into table data_raw_headless;
--check number of datarows
select count (stockcode) from data_raw_headless1 where stockcode!='';
-- result 541909
--cleaning of debris 
create table data_cleaned as select * from data_raw_headless1
where (quantity>0 AND unitprice>=0.0 AND customerid != '');
--confirmation and count of cleaned data
show tables;
select count (stockcode) from data_cleaned where stockcode!='';
-- result 397924
-- cleaned of debris 

-- analysis job 
create table kv_anlysis1(country string,totalcost float);  -- table for calculation of aggregate
insert into kv_anlysis1  select (country),(quantity*unitprice) from data_cleaned; -- population of table 
create table analysis1Result (country string,revAggr float); -- table reveneue aggregate of all countries
insert into analysis1Result select country,sum(totalcost) as revenue from kv_asses11 group by country order by revenue desc; --populating the table ordered 
create table analysis1T5 row format delimited fields terminated by '\t' stored as textfile as select * from analysis1Result order by revaggr desc limit 5; -- final required result; 

-- results obtained 
--** HIVE shell
--
--hive> select * from  analysis1T5;
--OK
--United Kingdom  7308391.5
--Netherlands     285446.34
--EIRE    265545.9
--Germany 228867.14
--France  209024.05
--Time taken: 0.211 seconds, Fetched: 5 row(s)
--hive> 
--** 
--
-- **HDFS CORE
--kali@kali:~$ hdfs dfs -cat /user/hive/warehouse/retaildb.db/analysis1t5/*
--Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
--2020-10-29 14:11:11,990 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
--United Kingdom  7308391.5
--Netherlands     285446.34
--EIRE    265545.9
--Germany 228867.14
--France  209024.05
--kali@kali:~$ 
--
