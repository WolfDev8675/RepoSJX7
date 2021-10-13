#!usr/bin/python

""" Module to help in plotting solutions """

#imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plts
import warnings as warns
import plotly.graph_objects as gr_objs

def manipulators(count,duplicated=True,repeated=True):
    """ Sets up permutation pairs """
    mnv=0
    mxv=count
    variations=[(i,j) for i in range(mnv,mxv) for j in range(mnv,mxv)]
    if not duplicated: 
        for k in range(mnv,mxv): variations.remove((k,k))
    if not repeated:
        for vars in variations: 
            if (vars[1],vars[0]) in variations: variations.remove(vars) 
    return variations


def singlePlot(plotter,X,Y,**kwargs):
    """ Definition and plotting with window 
    arrangements for a single plot 
    
    NB: this function is compatible with line, scatter, bar charts only

    *******************
    Variable list 
    ------------------
    plotter: function name definition to plot with 
    X : x variable ( iterable like* - multi dimensional )
    Y : y variable ( iterable like* - one dimensional   ) 

    *iterable like - must be a list/tuple/set, etc., likewise python primitives
    or numpy iterable objects or pandas iterable objects 
    ------------
    returns plot figure matplotlib.pyplot figure object 
    ____________________________
    Additional settings
       x_label: Abscissa axis label of the plot 
       y_label: Ordinate axis label of the plot
       title : Plot title or label heading of plot 
       window_dim : dimensions of the viewable window 
    
       ___________________*******___________________

    """
    warns.filterwarnings('ignore')
    xlabel,ylabel,title,window_dim=None,None,None,None;
    xlabel= kwargs['xlabel'] if 'xlabel' in kwargs else ' - X - '
    ylabel= kwargs['ylabel'] if 'ylabel' in kwargs else ' - Y - '
    title= kwargs['title'] if 'title' in kwargs else " Plot "
    window_dim= kwargs['window_dim'] if 'window_dim' in kwargs else (15,7.5)
    Fig=plts.figure(figsize=window_dim);ax=Fig.add_subplot(111);
    plotter(X,Y)
    plts.xlabel(xlabel);plts.ylabel(ylabel);plts.title(title);
    return plts.show()

def multiPlots(data,method=sns.scatterplot,unique_pairs=True):
    """ Plot multiple plots dpending on the requirements set
    ********************
    Variables 
    -------------------
    data :  pandas dataframe object 
    method : (deafult) sns.scatterplot -> plotting function  
    unique_pairs : (default) True -> plots of pairs, only those of which are unique
    
    ********************
    
    #need later revision in parameter usage and detailing for 'method' and 'grid' variable """
    
    # type error handling
    if type(data) is not pd.DataFrame: raise ValueError("Data type must be a pandas.Dataframe object")
    
    #Body
    cols=data.columns
    permutes=manipulators(len(cols),duplicated=False,repeated=False) if unique_pairs else manipulators(len(cols))
    plotFunc= method
    for a_pair in permutes:
        x_index= cols[a_pair[0]]
        y_index= cols[a_pair[1]]
        titled= x_index + ' vs ' + y_index
        singlePlot(plotFunc,data[x_index],data[y_index],xlabel=x_index,ylabel=y_index,title=titled,window_dim=(12,10))        
    print(' Plot Success ***** ')    

def fullDataPlots(data,method=sns.pairplot,title=None,window_dim=(15,10)):
    """ Plot functionalities for full dataset plots
     like pairplots and boxplots 
     ********************
    Variables 
    -----------------------
    data : pandas.DataFrame object
    method : sns plot function object  
    title : plot title
    ------------------------
    returns figure object  
    """
    figHandler=method(data=data);
    Fig=plts.gcf()
    Fig.set_figwidth(15)
    Fig.set_figheight(7.5)
    Fig.suptitle(title)
    plts.subplots_adjust(0.064,0.06,0.983,0.938)
    return plts.show()

def stockCandle(data,title=''):
    """ Create a Candlestick chart for stock market like data 
    *********************
    Variables
    ---------------------
    data : pandas.DataFrame object with specified definition type 
    title: title to the chart 
    
    Dataframe definition type must follow
    1. Date must be indexed 
    2. Date index must be a datetime object
    3. Must have 'Open','High','Low','Close' columns of data 
    _________________________
    returns a plotted candlestick chart with sliders 
    """
    Fig = gr_objs.Figure(data=[gr_objs.Candlestick(x=data.index,
                open=data.Open, high=data.High,
                low=data.Low, close=data.Close)],
                layout=gr_objs.Layout(title=gr_objs.layout.Title(text=title)))
    return Fig.show()

def residualsPlot(X,Y_t,Y_p,title,linefmt):
    """ Function plots for generating StemPlot natured residual plot
    *******************
    Variables 
    ----------------------
    X  : x axis values (array like)
    Y_t : y variable considered true (array like)
    y_p : y variable considered as predicted (array like)
        residuals are calculated as for each x the residue is calculated as (Y_t-Y_p) 
    title : the title to the corresponding plot 
    linefmt : the line format respective to the chart plotted 
    -------------------------
    returns matplotlib.container.StemContainer object 
    _____________________________
    """
    residuals=Y_t-Y_p;
    stems=plts.stem(X,residuals,linefmt=linefmt);plts.title(title);
    return stems 