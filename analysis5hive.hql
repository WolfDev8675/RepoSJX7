-- Analysis 5: 
-- ** Basket size distribution (Note: Basket size = number of items in a transaction) *
-- *  (in this questions, we would like to know that, number of transactions by each basket size *
-- *   i.e. number of transactions with 3 size, number of transactions with 4 size etc.)  **

-- start of codes
-- one time jobs 
-- **## Please avoid lines here on forward if retaildb is available in 'show databases' command and contains data                   ##**
-- **## if avoiding these lines till line 25 directly jump to codes in analysis section of the code which next to this section      ##**
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
-- Job: Basket Size 
create table kv_asses5 as select (invoiceno),(quantity) from data_cleaned;   -- kv pair invoiceno to quantity
create table analysis5result(invoiceno string,basket_size int); -- creating table for calculating results 
insert into analysis5result select invoiceno,sum(quantity) as basket from kv_asses5 group by invoiceno order by basket desc; -- populating table ;
--*;

-- end of code 

-- results obtained 
--** HIVE shell
--

--hive> select * from analysis5result limit 10;
--OK
--581483  80995
--541431  74215
--556917  15049
--563076  14730
--572035  13392
--567423  12572
--578841  12540
--552883  12266
--563614  12196
--562439  11848
--Time taken: 0.155 seconds, Fetched: 10 row(s)
--hive>
--
--***** note that for job the viewed results are limited to top 10 outputs to avoid printing all 18536 results ****
