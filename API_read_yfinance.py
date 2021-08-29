#!usr/bin/python

#API readers
"""***Imports***"""

import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plots

"""*Data access*"""

BrentCrude=yf.Ticker("BZ=F")
print(BrentCrude.info)
DTX_BrentC=BrentCrude.history(period="5y")
print(DTX_BrentC)
print(DTX_BrentC.info())

x=DTX_BrentC.index;
y=DTX_BrentC['Close'];
plots.plot(x,y)
plots.show()