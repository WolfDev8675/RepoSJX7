#!usr/bin/python

''' json file data '''
# start of code

# file source https://thingspeak.com/channels/129016

#imports
from file7_webScr import *
import json
import pandas as pd

# static collections
web_url='https://thingspeak.com/channels/129016/field/1.json'
destination_local='F:\BSE_2\VS_Reg_BSE'
filename_local='test_file.json'

#file access and storing
file_path=accessFile(web_url,destination_local,filename_local)
with open(file_path) as f_jsn:
    data=json.loads(f_jsn.read())

# print(data)

# info of location
data_info=data["channel"]
for data_key in data_info:
    print(data_key,"\t:\t",data_info[data_key])
#data body
data_body= pd.DataFrame(data["feeds"])
print(" ".center(50,'*'))
print(data_body)

