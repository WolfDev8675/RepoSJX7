# RepoSJX7 : branch Assign2_2
Project 2: Time Series Modelling of Bank Stock Price Pair

Data Set: Last two years daily trade data of HDFCBANK and ICICIBANK. Data can be obtained from 
- https://www.nseindia.com/get-quotes/equity?symbol=HDFCBANK
- https://www.nseindia.com/get-quotes/equity?symbol=ICICIBANK

Data Length: 273 trading days data consisting of LTP and Close price
Fields to be considered: LTP and Close Price.
Compute the daily price ratio using LTP and Close Price
Model the Ratio variable using suitable Time Series Modelling

Problem Statement: 
Devise a trading strategy using the stock price data as given. Specifically to identify the duration (or trading signal) when a stock will be kept in long position and the another one in short position. 
The trade set up should be market neutral and the positions will be taken simultaneously.  
Workaround:
Identify the values of p, q and d, in case we are using ARIMA(p,d,q) model. In this way, we identify the mean reversion of the ratio. In other words we need to find out the speed of mean reversion. 
Speed of Mean Reversion = HL = ln(2)/kappa where kappa is estimated from an AR(p) process. 
Secondly once we have identified the speed of mean reversion, trade is to be set up. In this case we need to identify using following formula the number of FUTURE contract we should go long and short.
Number of Contract * Lot Size * FutureContract_Price_StockA = Number of Contract * Lot Size * FutureContract_Price_StockB
In the above Lot Size and FutureContract_Price are to be obtained from NSE site. Solve for Number of Contract. 
Expected Output:
Identify the values of p,d and q
Performance Metrics of the ARIMA Model i.e RMSE. 
Number of Contracts required to set up the trade
Mean reversion speed. 

** Documentation of completed project https://github.com/WolfDev8675/RepoSJX7/blob/Assign2_2/timeSeries_project_doc.pdf
