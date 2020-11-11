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
--Job3: Average Number of items by Country for top 5
create table kvp_asses23 as select (country),(quantity) from data_cleaned;   -- kv pair country to quantity
create table analysis23result_t(country string,num_items int);    -- result master table for counter 
insert into analysis23result_t select country,sum(quantity) as total from kvp_asses23 group by country order by total desc; -- counting and ordering with insertion into table 
create table analysis23result(country string,average float); -- final table of results
insert into analysis23result select country,num_items/(select count(*) from analysis23result_t) as average from analysis23result_T order by average desc; -- final result 
create table analysis23T5 row format delimited fields terminated by '\t' stored as textfile as select * from analysis23result order by average desc limit 5 -- final required result with segregation and ordering
--*
--Job4,5,6: Minimum, Maximum, Average amount per customers
create table kv_asses2x456(customerid string,invoiceno string,inv_cost float); -- master table for calucltions of job 4,5,6.
insert into kv_asses2x456 select customerid,invoiceno,sum(quantity*unitprice) from data_cleaned group by invoiceno,customerid; -- populating table
create table analysis24result as select customerid,min(inv_cost) as minval from kv_asses2x456 group by customerid order by minval desc; -- minimum of orders
create table analysis25result as select customerid,max(inv_cost) as maxval from kv_asses2x456 group by customerid order by maxval desc; -- maximum of orders
create table analysis26result as select customerid,avg(inv_cost) as avgval from kv_asses2x456 group by customerid order by avgval desc; -- average of orders
--*
-- end of code 

-- results obtained 
--** HIVE shell
--

--hive> select * from analysis21T5;
--OK
--United Kingdom  3921
--Germany 94
--France  87
--Spain   30
--Belgium 25
--Time taken: 0.186 seconds, Fetched: 5 row(s)
--hive> select * from analysis22T5;
--OK
--United Kingdom  16649
--Germany 457
--France  389
--EIRE    260
--Belgium 98
--Time taken: 0.153 seconds, Fetched: 5 row(s)
--hive> select * from analysis23T5;
--OK
--United Kingdom  115391.13
--Netherlands     5430.7295
--EIRE    3797.973
--Germany 3223.3242
--France  3012.7568
--Time taken: 0.18 seconds, Fetched: 5 row(s)
--hive> select * from analysis24result limit 10;
--OK
--12346   77183.59
--15749   7837.5
--12357   6207.67
--12688   4873.81
--12752   4366.78
--18251   4314.7197
--12536   4161.06
--12378   4008.6199
--15195   3861.0
--12435   3850.9
--Time taken: 0.157 seconds, Fetched: 10 row(s)
--hive> select * from analysis25result limit 10;
--OK
--16446   168469.6
--12346   77183.59
--15098   38970.0
--17450   31698.16
--12415   22775.93
--18102   22206.0
--15749   21535.9
--14646   20277.92
--12931   18841.48
--14156   16774.72
--Time taken: 0.148 seconds, Fetched: 10 row(s)
--hive> select * from analysis26result limit 10;
--OK
--16446   84236.24687504768
--12346   77183.59375
--15749   14844.7666015625
--15098   13305.5
--12357   6207.669921875
--12415   5948.310857863653
--12590   4932.1298828125
--12688   4873.81005859375
--12752   4366.77978515625
--18102   4327.621684646607
--Time taken: 0.156 seconds, Fetched: 10 row(s)
--hive> 
--
--***** note that for jobs 4, 5, 6 the viewed results are limited to top 10 outputs to avoid printing all 4339 results ****
