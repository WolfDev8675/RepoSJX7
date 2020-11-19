#!usr/bin/python
#
# *******
# **    Analysis 3:                                                                            *
# *   Daily sales activity like numvisits, total amount monthly and quarterly for 1 year.**
# *******
# start of code
import sys 
for line in sys.stdin:
    row=line.strip()
    components=row.split("\t")
    try:
        if ( "" not in components and int(components[3])>= 0 and float(components[5])>= 0.0 ):
            
            # generating K,V pairs after filtering out debris in data
            print('%s\t%s\t%d\t%f'%(components[4],components[0],int(components[3]),float(components[5])))
        else:
           #print(components)
           continue
    except Exception:
        #print(components)
        continue
    

# end of code 
#results mentioned in reducer
