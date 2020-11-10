-- Analysis 2: 
-- Sales Metrics like NumCustomers, NumTransactions, AvgNumItems, MinAmtperCustomer, MaxAmtperCustomer, AvgAmtperCustomer.. by country for top 5 countries 

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
-- Job1: Number of customers by country for top 5 
create table kvp_asses21 as select distinct (country),(customerid) from data_cleaned;   -- kv pair country to customer id
create table analysis21result(country string,num_customers int);    -- result master table for counter 
insert into analysis21result select country,count(customerid) as counter from kvp_asses21 group by country order by counter desc; -- counting and ordering with insertion into table 
create table analysis21T5 row format delimited fields terminated by '\t' stored as textfile as select * from analysis21result order by num_customers desc limit 5 -- final required result with segregation and ordering
--*
--Job2: Number of transactions by Country for top 5
create table kvp_asses22 as select distinct (country),(invoiceno) from data_cleaned;   -- kv pair country to invoice number
create table analysis22result(country string,num_transact int);    -- result master table for counter 
insert into analysis22result select country,count(invoiceno) as counter from kvp_asses22 group by country order by counter desc; -- counting and ordering with insertion into table 
create table analysis22T5 row format delimited fields terminated by '\t' stored as textfile as select * from analysis22result order by num_transact desc limit 5 -- final required result with segregation and ordering
--*


