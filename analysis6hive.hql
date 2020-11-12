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
insert into kv_asses6 select concat(stockcode,'->',description),(quantity) from data_cleaned;   -- populating data 
create table analysis6result(items string,frequency int); -- creating table for calculating results 
insert into analysis6result select items,sum(quantity) as freq from kv_asses6 group by items order by freq desc; -- populating table 
create table analysis6T20 row format delimited fields terminated by '\t' stored as textfile 
as select * from analysis6result order by frequency desc limit 20; --final result ;
--*;

-- end of code 

-- results obtained 
--** HIVE shell
--

--hive> select * from analysis6t20;
--OK
--23843->"PAPER CRAFT , LITTLE BIRDIE"    80995
--23166->MEDIUM CERAMIC TOP STORAGE JAR   77916
--84077->WORLD WAR 2 GLIDERS ASSTD DESIGNS        54415
--85099B->JUMBO BAG RED RETROSPOT 46181
--85123A->WHITE HANGING HEART T-LIGHT HOLDER      36725
--84879->ASSORTED COLOUR BIRD ORNAMENT    35362
--21212->PACK OF 72 RETROSPOT CAKE CASES  33693
--22197->POPCORN HOLDER   30931
--23084->RABBIT NIGHT LIGHT       27202
--22492->MINI PAINT SET VINTAGE   26076
--22616->PACK OF 12 LONDON TISSUES        25345
--21977->PACK OF 60 PINK PAISLEY CAKE CASES       24264
--17003->BROCADE RING PURSE       22963
--22178->VICTORIAN GLASS HANGING T-LIGHT  22433
--15036->ASSORTED COLOURS SILK FAN        21876
--21915->RED  HARMONICA IN BOX    20975
--22386->JUMBO BAG PINK POLKADOT  20165
--22197->SMALL POPCORN HOLDER     18252
--20725->LUNCH BAG RED RETROSPOT  17697
--84991->60 TEATIME FAIRY CAKE CASES      17689
--Time taken: 0.153 seconds, Fetched: 20 row(s)
--hive> 
--
-- **** 
--
