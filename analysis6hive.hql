-- Analysis 6: 
-- Top 20 Items sold by frequency 

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

--Analysis Jobs 
--*
-- Job: Top 20 items sold by frequency 
create table kv_asses6 (items string,quantity int); -- kv pair items to quantity
insert into kv_asses6 select (stockcode+"\t"+description),(quantity) from data_cleaned;   -- populating data 
create table analysis6result(items string,frequency int); -- creating table for calculating results 
insert into analysis6result select items,sum(quantity) as freq from kv_asses6 group by items order by freq desc; -- populating table ;
--*;

-- end of code 

-- results obtained 
--** HIVE shell
--

--
