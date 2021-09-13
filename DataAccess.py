#!usr/bin/python

""" Module for accessing various amounts of data """

# Imports 

import pandas as pd
import yfinance as yf
import numpy as np
import warnings as warns
from datetime import datetime as dt

def data_Prestored(location):
    """  Get access to prestored data """
    dataHist=pd.read_csv(location,index_col='Date',)
    if 'Price' in dataHist.columns :
        dataHist.rename(columns={'Price':'Close'},inplace=True)
    return dataHist

def data_Live(ticker="BZ=F",period="2M"):
    """ Access or import live/current of a given stock """
    dataRaw=yf.Ticker(ticker)
    DFrame=dataRaw.history(period=period)
    return DFrame

def data_FixedTimeLine(ticker="BZ=F",start=None,end=None):
    """ Access or import stock data of a fixed timeline """
    if start is None or end is None:
        warns.warn(" Start or End limit must have some values, it shouldn't be (None) ",category=SyntaxWarning)
        if start is None and end is not None:
            dataRaw=yf.download(ticker,start=dt.now().date(),end=end)
        if start is not None and end is None:
            dataRaw=yf.download(ticker,start=start,end=dt.now().date())
        if start is None and end is None:    
            dataRaw=yf.Ticker(ticker).history()
    else:
        dataRaw=yf.download(ticker,start=start,end=end)
    return dataRaw