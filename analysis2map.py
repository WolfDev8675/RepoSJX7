#!usr/bin/python
#
# *******
# **    Analysis 2:                                                                            *
# *   Sales Metrics like NumCustomers, NumTransactions, AvgNumItems,                          **
# *    MinAmtperCustomer, MaxAmtperCustomer, AvgAmtperCustomer, StdDevAmtperCustomer, etc.    **
# *     by country for top 5 countries                                                        **
# *******
# start of code
import sys 
for line in sys.stdin:
    row=line.strip()
    components=row.split("\t")
    try:
        if ( "" not in components and int(components[3])>= 0 and float(components[5])>= 0.0 ):
            
            # generating K,V pairs after filtering out debris in data
            print('%s\t%s\t%d\t%f\t%s'%(components[7],components[0],int(components[3]),float(components[5]),components[6]))
        else:
           #print(components)    # debug lines for error testing in code
           continue           #ignore condition failures -> quality control
    except Exception:
        #print(components)      # debug lines for error testing in code
        continue              #ignore condition failures -> quality control
    
# end of code 
# results mentioned in the specific reducer 
