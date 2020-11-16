#!usr/bin/python
#
#   Analysis 6: 
#       Top 20 Items sold by frequency
#  start of code
import sys   
for line in sys.stdin:      
    row=line.strip()    # removeing white spaces
    components=row.split("\t")      # separating individual components 
    try:
        if ( "" not in components and int(components[3])>= 0 and float(components[5])>= 0.0 ):   # filtration -> quality control 
            print('%s\t%d'%(components[1]+'->'+components[2],int(components[3])))   # key: item ; values : quantity
        else:
            continue   #ignore condition failures -> quality control
    except Exception:
        continue    # ignore filtration failure -> quality control 
    
# end of code 
# results mentioned in the reducer 
