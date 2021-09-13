#!usr/bin/python

#API readers
"""***Imports***"""

import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plots
from statsmodels.tsa.seasonal import seasonal_decompose

"""*Data access*"""

BrentCrude=yf.Ticker("BZ=F")
#print(BrentCrude.info)
DTX_BrentC=BrentCrude.history(period="2Y")
print(DTX_BrentC)
print(DTX_BrentC.info())

x=DTX_BrentC.index;
y=DTX_BrentC['Close'];
plots.plot(x,y)
plots.show()

model_TS=seasonal_decompose(DTX_BrentC[['Close']],model='additive',period=30)
model_TS.plot()
plots.show() 