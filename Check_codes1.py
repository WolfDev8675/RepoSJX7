#!usr/bin/python

""" Code for editing place details using GPS locations
 for file 'place details.csv' """
# code file: PlaceEdits.py
# code author: BishalBiswas(https://github.com/WolfDev8675)

#imports 
import pandas as PD
from geopy.geocoders import Nominatim as G_Loc


# DataFrame
placeDF=PD.read_csv('e:\Source\Repos\WolfDev8675\RepoSJX7\Data\place details.csv',encoding='latin-1')

# operate 
citydct={}
countydct={}
citydct["Excepts"]=0
countydct["Excepts"]=0

idx=placeDF.index.to_list()
GeoLoc=G_Loc(user_agent='Generic')
for one_id in idx:
  lat=str(placeDF.loc[one_id,'latitude'])
  lon=str(placeDF.loc[one_id,'longitude'])
  plc=GeoLoc.reverse(lat+","+lon).raw['address']
  
  try:
      #placeDF.loc[one_id,'city']=plc['city']
      if plc['county'] not in countydct: countydct[plc['county']]=1
      else: countydct[plc['county']]+=1
  except:
      countydct["Excepts"]+=1
      
  try:
      if plc['city'] not in citydct: citydct[plc['city']]=1
      else: citydct[plc['city']]+=1
  except:
      citydct["Excepts"]+=1


print(citydct)
#placeDF.to_csv("e:\Source\Repos\WolfDev8675\RepoSJX7\EditedData\place details.csv") 
print(countydct)
