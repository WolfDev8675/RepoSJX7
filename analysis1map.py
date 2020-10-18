##** VisualStudio2019 code
#!usr/bin/python
#
#   Analysis 1: 
#       Mapper for isolating components of Revenue Aggregrate *
#           by country for top 5 countries  **
import sys 

for line in sys.stdin:
    row=line.strip()
    components=row.split("\t")
    if int(components[3])>= 0 or float(components[5])>= 0.0 :
        print('%s,%d,%f'%(components[7],int(components[3]),float(components[5]))

   


# end of code 

##** KomodoIDE code
#!usr/bin/python
#
#   Analysis 1: 
#       Mapper for isolating components of Revenue Aggregrate *
#           by country for top 5 countries  **
import sys 

for line in sys.stdin:
    row=line.strip()
    components=row.split('\t')
    if int(components[3])>= 0 or float(components[5])>= 0.0 :
        print('%s,%d,%f'%(components[7],int(components[3]),float(components[5]))
    else:
       continue



# end of code 
