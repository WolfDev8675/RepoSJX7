-- Analysis 4: 
-- ** Hourly sales activity like numvisits, totalamount per hour of day. ***

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
-- Job1: NumVisits monthly 
create table kv_asses41(timeval bigint, invoiceno string); -- creating schema kv pair timestamp to invoice 
insert into kv_asses41 select distinct (unix_timestamp(invoicedate,'yyyy-MM-dd HH:mm')),invoiceno from data_cleaned; -- populating table 
create table hourlyhits(dayhr string,invoice string); -- segregation table schema 
insert into hourlyhits select concat(to_date(from_unixtime(timeval)),'->',hour(from_unixtime(timeval))), invoiceno from kv_asses41; -- filling
create table soln41 as select dayhr,count(invoice) from hourlyhits group by dayhr order by dayhr; -- final result ;

--Job2: TotalCosts monthly 
create table kv_asses42(timeval bigint, totalcost float); -- creating schema kv pair timestamp to cost 
insert into kv_asses42 select (unix_timestamp(invoicedate,'yyyy-MM-dd HH:mm')),(quantity*unitprice) from data_cleaned; -- populating table 
create table hourlycosts(dayhr string,costs float); -- segregation table schema 
insert into hourlycosts select concat(to_date(from_unixtime(timeval)),'->',hour(from_unixtime(timeval))), totalcost from kv_asses42; -- filling 
create table soln42 as select dayhr,sum(costs) from hourlycosts group by dayhr order by dayhr; -- final result;

--*;

-- end of code 

-- results obtained 
--** HIVE shell
--

-- Number of visits per hour
--hive> select * from soln41 limit 10; 
--OK
--2010-12-01->10  11
--2010-12-01->11  12
--2010-12-01->12  22
--2010-12-01->13  12
--2010-12-01->14  8
--2010-12-01->15  14
--2010-12-01->16  17
--2010-12-01->17  4
--2010-12-01->8   6
--2010-12-01->9   16
--Time taken: 0.142 seconds, Fetched: 10 row(s)
--hive> 


--Total costs per hour 
--hive> select * from soln42 limit 10; 
--OK
--2010-12-01->10  5235.810002326965
--2010-12-01->11  4234.159994512796
--2010-12-01->12  7447.920057356358
--2010-12-01->13  5063.539980441332
--2010-12-01->14  2831.219994932413
--2010-12-01->15  3587.3099961280823
--2010-12-01->16  8623.14000633359
--2010-12-01->17  613.190004825592
--2010-12-01->8   1383.8100109100342
--2010-12-01->9   7356.389957070351
--Time taken: 0.174 seconds, Fetched: 10 row(s)
--hive> 

--*******
