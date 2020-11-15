# RepoSJX7
Hadoop BIGDATA assignments (BSE+MAKAUT)
Data defined in https://www.kaggle.com/minatverma/nse-stocks-data?select=FINAL_FROM_DF.csv 
## Questions:

1 Use the given csv file as input data and implement following transformations:
    Filter Rows on specified criteria "Symbol equals GEOMETRIC"
    Select specific columns from those available: SYMBOL, OPEN, HIGH, LOW and CLOSE which meets above criteria
    Generate count of the number of rows from above result

2 Calculation of various statistical quantities and decision making:
    Only lines with value "EQ" in the "series" column should be processed. As the first stage, filter out all the lines that do not fulfil this criteria.
    For every stock(with value "EQ" in the "series"), for every year, calculate the statistical parameters(Minimum, Maximum, Mean and Standard Deviation) and store the generated information in properly designated tables.

3 Select any year for which data is available:
    For the selected year, create a table that contains data only for those stocks that have an average total traded quntity of 3 lakhs or more per day. Print out the first 25 entries of the table and submit.
    From above output, select any 10 stocks from IT ('HCLTECH', 'NIITTECH', 'TATAELXSI','TCS', 'INFY', 'WIPRO', 'DATAMATICS','TECHM','MINDTREE' and 'OFSS') and create a table combining their data.
    Find out the Pearsons Correlation Coeffecient for every pair of stocks you have selected above. Final output should be in decreasing order of the coeffecient.

4. Use the coorrelation information generated in step 3 in the following way:
    a. Assume you have Rs10 lakh to invest 
    b. Assume you have to invest in six stocks on the first working day of January of the next year.
    c. By using logic/simulation/etc. Identify the stocks that you will invest in, such that at the end of the year:
      At least your overall capital (Rs 10 lakh) is protected. 
      
