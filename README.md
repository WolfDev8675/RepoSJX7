# RepoSJX7
Hadoop BIGDATA assignments (BSE+MAKAUT)
Job specified on OnlineRetail file.. file is not uploadable to Git since file exceeds 25MB
**Quesion set and assignment detailing**
Retail Sales Analytic
Overview:
  The objective of the project to illustrate retail analytics using an online retail dataset containing transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail. This dataset is used to demonstrate an end-to-end retail analytic use case on the Hadoop Data Platform distribution: 
*Data ingestion and cleansing using Apache Pig/Hive/Map Reduce(pyhthon)/Spark/HBASE*
  *5 hrs*
Data set:
  InvoiceNo-integer -Transaction Number
  StockCode-character -SKU Code (Product Code)
  Description -character -Product Description
  Quantity -int-Quantity ordered
  InvoiceDate-character -Transaction Data
  UnitPrice-float-Price per unit quantity
  CustomerID-character -Customer ID
  Country -character -Customer location
*Analysis:*
1.Revenue Aggregate By Country for top 5 countries
2.Sales Metrics like NumCustomers, NumTransactions, AvgNumItems, MinAmtperCustomer, MaxAmtperCustomer, AvgAmtperCustomer,
StdDevAmtperCustomeretc. .. by country for top 5 countries
3.Daily Sales Activity like NumVisits, TotalAmtetc… per POSIX day of the year
4.Hourly sales Activity like NumVisits, TotalAmtetc… per hour of day
5.Basket size distribution (Note: Basket size = number of items in a transaction) ( in this questions, we would like to know that, number of transactions by each basket size i.e. number of transactions with 3 size, number of transactions with 4 size etc.
6.Top 20 Items sold by frequency
7.Customer Lifetime Value distribution by intervals of 1000’s (Customer Life time Value = total spend by customer in his/her tenure with the company) (In this question, we would like to calculate how many customers with CLV between 1-1000, 1000-2000 etc.). Please note that we don’t want calculate bins manually and it required to create bins dynamically.
