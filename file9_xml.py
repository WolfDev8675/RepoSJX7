#!usr/bin/python

''' xml file data '''
# start of code

# file source https://thingspeak.com/channels/129016

#imports
from file6_webScr import *
import xml.etree.ElementTree as et
import pandas as pd

# static collections
web_url='https://thingspeak.com/channels/129016/field/1.xml'
destination_local='F:\BSE_2\VS_Reg_BSE'
filename_local='test_file.xml'

#parsing and root access
xml_file=et.parse(accessFile(web_url,destination_local,filename_local))
file_root=xml_file.getroot()

# xml print 
#for gen0 in file_root:
#    print(gen0.tag,'***',gen0.text)
#    for gen1 in gen0:
#        print(gen1.tag,">>>")
#        for gen2 in gen1: 
#            print(gen2.tag,"^^",gen2.text)



# framing up with assimilation 
data_colec=[]
data_dict={} 
for gen0 in file_root:
    print(gen0.tag,'***',gen0.text)
    for gen1 in gen0:
        data_dict={} # level inialize
        for gen2 in gen1: 
            data_dict[gen2.tag]=gen2.text
        data_colec.append(data_dict) # post write 

# generating dataframe
data_body= pd.DataFrame(data_colec)
print(" ".center(50,'*'))
print(data_body)


