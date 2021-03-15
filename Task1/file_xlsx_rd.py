#!usr/bin/python

''' Read an XLSX file and push it into a pandas dataframe '''

# Data obtained by download and conversion to XLS file from https://data.sa.gov.au/data/dataset/metro-median-house-sales/resource/8f2d0be3-3b36-432f-ae84-c459c3e426cc
# start of code

# imports 
import pandas as pd

# destination path fix and file names 
final_path = r'E:\Downloads'
fl_name="AussieDataHousing.xlsx"
complete_path= final_path+"\\"+fl_name

# DataFrame implementation
dFrame=pd.read_excel(complete_path)
print(dFrame)

# end of code


#output 
"""

      id            City  ... Median\n4Q 2020  Median\nChange
0      1        ADELAIDE  ...        864750.0          0.1229
1      2        ADELAIDE  ...       1600000.0          0.1830
2      3  ADELAIDE HILLS  ...        863750.0          0.1501
3      4  ADELAIDE HILLS  ...             NaN             NaN
4      5  ADELAIDE HILLS  ...             NaN             NaN
..   ...             ...  ...             ...             ...
474  475    WEST TORRENS  ...        654000.0         -0.1309
475  476    WEST TORRENS  ...        705000.0          0.0973
476  477    WEST TORRENS  ...        605000.0          0.0067
477  478    WEST TORRENS  ...        875000.0          0.0789
478  479    WEST TORRENS  ...        388500.0             NaN

[479 rows x 8 columns]
Press any key to continue . . .

"""