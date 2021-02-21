import org.apache.spark._
import org.apache.log4j._
import org.apache.spark.sql.Row
import org.apache.spark.sql.types._
import org.apache.spark.sql.functions._
import org.apache.spark.sql._
import org.apache.spark.sql._
object BSE_Project_Retail {
  case class RETAIL_SCHEMA(
Invoice:String, StockCode:String, Description:String, Quantity:Int, InvoiceDate:String, Price:Double, Customer_ID:String, Country:String)
  def main(args: Array[String]) {
    Logger.getLogger("org").setLevel(Level.ERROR)
    val sc = new SparkContext("local[*]", "OnlineRetails")
    val spark = SparkSession.builder.appName("OnlineRetail").master("local[*]").getOrCreate()
    import spark.implicits._
    val retail_ds = spark.read.option("header", "true").option("inferSchema", "true").csv("data/online_retail_headers.csv").cache().as[RETAIL_SCHEMA]
    val retail_fil = retail_ds.filter($"Price" >= 0 and $"Quantity" > 0 and $"StockCode" === "85123A" and
        $"Country".isNotNull and 
        $"Invoice".isNotNull and 
        $"StockCode".isNotNull and 
        $"InvoiceDate".isNotNull and
        $"Customer_ID".isNotNull)
    val final_filtered_data = retail_fil.select($"Customer_ID", $"Quantity", $"Price", $"InvoiceDate", $"Country", $"StockCode")
   

val group_by = final_filtered_data.groupBy($"Customer_ID").
                                   agg(sum("Price").as("SUM_PRICE"), 
                                       sum("Quantity").as("TOTAL_QUANTITY"), 
                                       count("Quantity").as("PURCHASE_COUNT"), 
                                       max("InvoiceDate").as("MAX_DATE")).                   withColumn("USER_DATE",to_timestamp(lit("20111204"),"yyyyMMdd")).
              withColumn("mdate",date_format(unix_timestamp(col("MAX_DATE"),"dd-MM-yyyy HH:mm").cast(TimestampType), "yyyy-MM-dd HH:mm:ss"))
val final_output = group_by.select($"Customer_ID", $"SUM_PRICE", $"TOTAL_QUANTITY", $"PURCHASE_COUNT",$"MAX_DATE", (datediff(col("USER_DATE"),col("mdate"))/365).as("RECENCY")).
                withColumn("Y", when(col("PURCHASE_COUNT") > 2,1).otherwise(0))
    final_output.show()
    print(final_output.count())
    final_output.repartition(1).write.format("csv").option("header", "true").save("data/retail_final_filter_data")
  }
}

//End of codes...
