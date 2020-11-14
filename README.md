# RepoSJX7
Hadoop BIGDATA assignments (BSE+MAKAUT)
Data defined in https://www.kaggle.com/minatverma/nse-stocks-data?select=FINAL_FROM_DF.csv 
## Questions:
1. Using data provide as input data implement transformations that should happen during mapping and reducingstagesto implement each of the following operations:
a. Filter rows of a table based on the specific criteria "SYMBOL equals GEOMETRIC"
b. Select specific columns from those available (eg. SELECT SYMBOL, OPEN, HIGH, LOW, CLOSE)
c. Generate a count of the number of rows in the table

2.Calculations of various statistical quantities and decision 
  1. Only lines with value "EQ" in the "Series" column should be processed. As the first stage, filter out all lines that do not fulfil this criteria.
  2. For every stock, for every year, calculate the following statistical parameters and store the generated information in properly designed tables: Min, Max, Mean, StandardDeviation
  3. Select any year for which data is available. In your report clearly mention the year selected 
    a. for that year, create a table that contains data only for those stocks that have an average total traded quantity of 3 lakhs or more per day. Print out the first 25 entries of the Table and submit 
    b. From among these, select any 10 stocks from IT(eg. INFY, WIPRO, TCS, GEOMETRIC, etc.) and create a Table containing their data
    c. Find out Pearsons Correlation Coefficient for Every pair of stocks you have selected. Final output should be in decreasing order of the coefficient.
  4. Use the coorrelation information generated in step 3 in the following way:
    a. Assume you have Rs10 lakh to invest 
    b. Assume you have to invest in six stocks on the first working day of January of the next year.
    c. By using logic/simulation/etc. Identify the stocks that you will invest in, such that at the end of the year:
      At least your overall capital (Rs 10 lakh) is protected. 
      
