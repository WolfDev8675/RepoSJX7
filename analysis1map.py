#!usr/bin/python
#
#   Analysis 1: 
#       Mapper for isolating components of Revenue Aggregate *
#           by country for top 5 countries  **
#  start of code
import sys   
for line in sys.stdin:      
    row=line.strip()    # removeing white spaces
    components=row.split("\t")      # separating individual components 
    try:
        if ( "" not in components or int(components[3])>= 0 or float(components[5])>= 0.0 ):   # filtration -> quality control 
            print('%s,%d,%f'%(components[7],int(components[3]),float(components[5])))   # key: country ; values : quantity and unit price
        else:
            continue   #ignore condition failures -> quality control
    except Exception:
        continue    # ignore filtration failure -> quality control 
    
# end of code 
