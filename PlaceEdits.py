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
idx=placeDF.index.to_list()
GeoLoc=G_Loc(user_agent='Generic')
for one_id in idx:
  lat=str(placeDF.loc[one_id,'latitude'])
  lon=str(placeDF.loc[one_id,'longitude'])
  plc=GeoLoc.reverse(lat+","+lon).raw['address']
  
  try:
      placeDF.loc[one_id,'city']=plc['city']
  except:
      placeDF.loc[one_id,'city']=plc['county'] # since counties are found to be city equivalent matching state outlines perfectly in this case
      # the classical case of city regions being shared between city municipality and another smaller neighbouring municipality
  
#push to secondary source 
placeDF.to_csv("e:\Source\Repos\WolfDev8675\RepoSJX7\EditedData\place details.csv", encoding='latin-1', index=False)
