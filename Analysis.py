#!usr/bin/python

""" Module for handling Statistical analysis of data """


#imports
from statsmodels.tsa.seasonal import seasonal_decompose
from Visuals import singlePlot,sns,warns,plts
from DataAccess import pd,dt

def trendNseasonality(data,model='additive',period=30):
    """ Visually discuss trend and seasonality of data """

    model_TS=seasonal_decompose(data,model='additive',period=30)
    #Fig=plts.figure(figsize=(15,7.5))
    Fig=model_TS.plot()
    Fig.suptitle(" Trend and Seasonality in the Data ")
    Fig.set_figwidth(15)
    Fig.set_figheight(7.5)
    plts.subplots_adjust(0.07,0.08,0.977,0.94)
    return plts.show()

def yearVariation(data,year):
    """ Generate visual statistics of variation of a time-series data with year """
    data_local=data[data.index.year==year]
    cols=data.columns
    Fig=plts.figure(figsize=(15,7.5));ax=Fig.add_subplot(111);
    sns.lineplot(data=data_local)
    plts.xlabel('Year : %d'%year)
    plts.title(str(list(cols))[2:-2]+' for '+str(year))
    return plts.show()
        




