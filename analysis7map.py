#!usr/bin/python
#
#   Analysis 7: 
# ** Customer Lifetime Value distribution by intervals of 1000’s (Customer Life time Value = total spend by customer in his/her tenure with the company) *
# * (In this question, we would like to calculate how many customers with CLV between 1-1000, 1000-2000 etc.). *
# * Please note that we don’t want calculate bins manually and it required to create bins dynamically. **

#  start of code
import sys   
for line in sys.stdin:      
    row=line.strip()    # removeing white spaces
    components=row.split("\t")      # separating individual components 
    try:
        if ( "" not in components and int(components[3])>= 0 and float(components[5])>= 0.0 ):   # filtration -> quality control 
            print('%s\t%f'%(components[6],int(components[3])*float(components[5])))   # key: invoice ; values : quantity
        else:
            continue   #ignore condition failures -> quality control
    except Exception:
        continue    # ignore filtration failure -> quality control 
    
# end of code 
# results mentioned in the reducer 
