#!usr/bin/python

# Analysis4:
#  Use the coorrelation information generated in step 3 in the following way:
# a. Assume you have Rs10 lakh to invest 
# b. Assume you have to invest in six stocks on the first working day of January of the next year. 
# c. By using logic/simulation/etc. Identify the stocks that you will invest in, such that at the end of the year: At least your overall capital (Rs 10 lakh) is protected.

import pandas as pd

df = pd.read_csv(r"C:\Users\Asus\Desktop\q2_2.csv",sep='\t')
df.columns = ['SYMBOL','MIN','MAX','AVG','STDEV','YEAR']

dfcor = pd.read_csv(r"C:\Users\Asus\Desktop\q2_3_3.csv",sep='\t',header=None)

l = []
lrate = []
for i in dfcor.iloc[:,0]:
    avg2011 = int(df[(df['SYMBOL'] == i) & (df['YEAR'] == 2011)]['AVG'])
    avg2013 = int(df[(df['SYMBOL'] == i) & (df['YEAR'] == 2013)]['AVG'])
    l.append(((avg2013-avg2011)/avg2011)*100)
    lrate.append()

dfcor.insert(1,'5',l)

dfcor.columns = ['SYMBOL1','%GROWTH',"SYMBOL2",'CORR_BW_S1andS2']

dfcor[dfcor['%GROWTH'] > 50].sort_values('%GROWTH')['SYMBOL1'].unique()
#Out[91]: array(['TCS', 'TECHM', 'HCLTECH', 'MINDTREE'], dtype=object)
#This list is in ascending order of GROWTH

dfcor[dfcor['%GROWTH'] > 50]
dfnse = pd.read_csv(r"C:\Users\Asus\Desktop\all.csv",
                    usecols=[0,1,2,3,4,5,6,7,8,9,10])

#LIST OF STOCKS THAT I WILL BUY
lbuy = ['MINDTREE','TCS','INFY','OFSS','TECHM' , 'HCLTECH']

lbuy2014JAN = []
lbuy2014DEC = []

for i in lbuy:
    jan2014 = int(dfnse[(dfnse['SYMBOL']==i) & 
                        (dfnse['TIMESTAMP'] == '01-JAN-2014')]['CLOSE'])
    
    dec2014 = int(dfnse[(dfnse['SYMBOL']==i) & 
                        (dfnse['TIMESTAMP'] == '01-DEC-2014')]['CLOSE'])
    lbuy2014JAN.append(jan2014)
    lbuy2014DEC.append(dec2014)

lbuy
#Out[115]: ['MINDTREE', 'TCS', 'INFY', 'OFSS', 'TECHM', 'HCLTECH']


lbuy2014JAN
#Out[116]: [1549, 2153, 3468, 3274, 1828, 1258]

lbuy2014DEC
#Out[117]: [1244, 2692, 4349, 3444, 2653, 1671]
