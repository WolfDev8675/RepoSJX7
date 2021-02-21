#!usr/bin/python

''' test file for checking web access of data and unzipping files in addition to reading of csv files to pandas.dataframe object '''
# start of code

# imports 
import pandas as pd
from zipfile import ZipFile as ZF

# destination path fix and file names 
final_path = r'F:\BSE_2\VS_Reg_BSE\test1'
fl_name="GlobalLandTemperaturesByMajorCity.csv"
complete_path= final_path+"\\"+fl_name

#specific unzip to a specific path
with ZF("F:\BSE_2\GlobalLandTemperatures.zip") as zip_extract:
    zip_extract.namelist()
    zip_extract.extract(fl_name,fr'{final_path}')

dFrame=pd.read_csv(complete_path)
print(dFrame)

# end of code


#output 
""" 

                dt  AverageTemperature  ...  Latitude Longitude
0       1849-01-01              26.704  ...     5.63N     3.23W
1       1849-02-01              27.434  ...     5.63N     3.23W
2       1849-03-01              28.101  ...     5.63N     3.23W
3       1849-04-01              26.140  ...     5.63N     3.23W
4       1849-05-01              25.427  ...     5.63N     3.23W
           ...                 ...  ...       ...       ...
239172  2013-05-01              18.979  ...    34.56N   108.97E
239173  2013-06-01              23.522  ...    34.56N   108.97E
239174  2013-07-01              25.251  ...    34.56N   108.97E
239175  2013-08-01              24.528  ...    34.56N   108.97E
239176  2013-09-01                 NaN  ...    34.56N   108.97E

[239177 rows x 7 columns]
Press any key to continue . . .
"""

#***********
