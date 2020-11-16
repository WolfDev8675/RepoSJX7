#!usr/bin/python
#
#   Analysis 5: 
#       Basket size distribution (Note: Basket size = number of items in a transaction) **
#       (in this questions, we would like to know that, number of transactions by each basket size) ** 
#       i.e. number of transactions with 3 size, number of transactions with 4 size etc. **
#  start of code
import sys   
for line in sys.stdin:      
    row=line.strip()    # removeing white spaces
    components=row.split("\t")      # separating individual components 
    try:
        if ( "" not in components and int(components[3])>= 0 and float(components[5])>= 0.0 ):   # filtration -> quality control 
            print('%s\t%d'%(components[0],int(components[3])))   # key: invoice ; values : quantity
        else:
            continue   #ignore condition failures -> quality control
    except Exception:
        continue    # ignore filtration failure -> quality control 
    
# end of code 
# results mentioned in the reducer 
