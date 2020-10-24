 data_raw= LOAD '/home/kali/Hadoop/Local_Datasets/OnlineRetail.txt' USING PigStorage() as (InvoiceNo:chararray,StockCode:chararray,Description:chararray,Quantity:int,InvoiceDate:Datetime,UnitPrice:float,CustomerID:chararray,Country:chararray);
 
