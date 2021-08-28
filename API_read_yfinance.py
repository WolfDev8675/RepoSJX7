#!usr/bin/python

#API readers
"""***Imports***"""

import pandas as pd
import yfinance as yf

"""*Data access*"""

BrentCrude=yf.Ticker("BZ=F")
print(BrentCrude.info)
DTX_BrentC=BrentCrude.history(period="5y")
print(DTX_BrentC)