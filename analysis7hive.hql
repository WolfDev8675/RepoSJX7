-- Analysis 7: 
-- ** Customer Lifetime Value distribution by intervals of 1000’s (Customer Life time Value = total spend by customer in his/her tenure with the company) *
-- * (In this question, we would like to calculate how many customers with CLV between 1-1000, 1000-2000 etc.). *
-- * Please note that we don’t want calculate bins manually and it required to create bins dynamically. **

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
-- Job: Customer Lifetime Value distribution by intervals of 1000’s
create table kv_asses7(customerid string,totalcost float);  -- table for calculation of customer lifetime value
insert into kv_asses7  select (customerid),sum(quantity*unitprice) as clv from data_cleaned group by customerid order by clv; -- population of table 

