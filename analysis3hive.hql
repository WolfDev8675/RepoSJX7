-- Analysis 3: 
-- ** Daily sales activity like numvisits, totalamount monthly and quarterly for 1 year ***

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
create table kv_asses31(timeval bigint, invoiceno string); -- creating schema kv pair timestamp to invoice 
insert into kv_asses31 select distinct (unix_timestamp(invoicedate,'yyyy-MM-dd HH:mm')),invoiceno from data_cleaned; -- populating table 
create table monthlyhits(month int,invoice string); -- segregation table schema 
insert into monthlyhits select month(from_unixtime(timeval)), invoiceno from kv_asses31;
create table soln31 as select month,count(invoice) from monthlyhits group by month order by month; -- final result ;

-- Job2: NumVisits quarterly
create table quarterlyhits (quarter int,invoice string); --segregation table schema 
insert into quarterlyhits select floor((month(from_unixtime(timeval))-0.1)/3), invoiceno from kv_asses31; -- filling up 
create table soln32 as select quarter,count(invoice) from quarterlyhits group by quarter order by quarter; -- final result ;

--Job3: TotalCosts monthly 
create table kv_asses32(timeval bigint, totalcost float); -- creating schema kv pair timestamp to cost 
insert into kv_asses32 select (unix_timestamp(invoicedate,'yyyy-MM-dd HH:mm')),(quantity*unitprice) from data_cleaned; -- populating table 
create table monthlycosts(month int,costs float); -- segregation table schema 
insert into monthlycosts select month(from_unixtime(timeval)), totalcost from kv_asses32; -- filling 
create table soln33 as select month,sum(costs) from monthlycosts group by month order by month; -- final result;

-- Job4: TotalCosts quarterly
create table quarterlycosts (quarter int,costs float); --segregation table schema 
insert into quarterlycosts select floor((month(from_unixtime(timeval))-0.1)/3), totalcost from kv_asses32; -- filling up 
create table soln34 as select quarter,sum(costs) from quarterlycosts group by quarter order by quarter; -- final result ;
--*;

-- end of code 

-- results obtained 
--** HIVE shell
--

-- Number of visits per month 
--hive> select * from soln31;
--OK
--1       993
--2       1003
--3       1324
--4       1153
--5       1559
--6       1394
--7       1331
--8       1283
--9       1757
--10      1930
--11      2660
--12      2179
--Time taken: 0.155 seconds, Fetched: 12 row(s)
--hive> 

-- Number of visits per quarter 
--hive> select * from soln32;
--OK
--0       3320
--1       4106
--2       4371
--3       6769
--Time taken: 0.161 seconds, Fetched: 4 row(s)
--hive> 

-- Total Costs  Monthly 
--hive> select * from soln33;
--OK
--1       569445.0322882384
--2       447137.3490101546
--3       595500.7586191893
--4       469200.3588609899
--5       678594.5577653646
--6       661213.6881134436
--7       600091.0089869479
--8       645343.8979516104
--9       952838.3793331122
--10      1039318.7866888493
--11      1161817.3760578
--12      1090906.6718007103
--Time taken: 0.169 seconds, Fetched: 12 row(s)
--hive> 


-- Total Costs Quarterly 
--hive> select * from soln34;
--OK
--0       1612083.1399175823
--1       1809008.6047397982
--2       2198273.286271671
--3       3292042.8345473595
--Time taken: 0.16 seconds, Fetched: 4 row(s)
--hive> 


--********
