#!usr/bin/python

""" HTML data extraction """ 
# start of codes...

# File source :: https://store.steampowered.com/search/?sort_by=_ASC&vrsupport=102
# Source descrition:
#  All softwares and tools available from STEAM store that has 
#  Oculus Rift support or can run on hardware of the equal origins
#  :: ** THIS IS TO BE NOTED THAT STEAMPOWERED.COM is only allowing
#  only the top 50 to be pulled at a time and even with multiple reloads
#   only pulls the first 50 items in the list. Unlike the browser where 
#   the page loads the additionals on scrolling down the webpage **
# ........

from file_webScrUL3 import *
from lxml import html as HT
import pandas as PD

webpath="https://store.steampowered.com/search/?sort_by=_ASC&vrsupport=102"
destination_local="\local"
filename_local="file.html"

# creating local copy 
filepath=accessFile(webpath,destination_local,filename_local)
with open(filepath) as f_htm:
    data=f_htm.read()

# initialize primary stages 
column_list=["Name","Platforms","VR","Release","Reviews","Discount","Price"]
dataByIndex=[] 

# HTML Tree Generation
plants=HT.fromstring(data) 
counter=1 #primary value 

#Extraction
while(counter):
    try:
        Name=plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div/div[3]/a["+str(counter)+"]/div[2]/div[1]/span")[0].text_content()
        span=1          #presetting values
        Platforms=[]
        while span:     # single to multiple platforms all embedded in a single paragraph with the VR information
            try:
                a_platform=str(list(plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div[2]/div[3]/a["+str(counter)+"]/div[2]/div[1]/p/span["+str(span)+"]")[0].values())[0]).split()[1]
                span+=1
                Platforms.append(a_platform)
            except: break # end of platforms 
        VR=plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div[2]/div[3]/a["+str(counter)+"]/div[2]/div[1]/p/span["+str(span)+"]")[0].text_content()
        Release=plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div[2]/div[3]/a["+str(counter)+"]/div[2]/div[2]")[0].text_content()
        Reviews=str(list(plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div[2]/div[3]/a["+str(counter)+"]/div[2]/div[3]/span")[0].values())[0]).split()[1]
        Discount=plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div[2]/div[3]/a["+str(counter)+"]/div[2]/div[4]/div[1]")[0].text_content().strip()
        if Discount: pass # available discounts (- discount %)
        else: Discount=0
        Price=plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div/div[3]/a["+str(counter)+"]/div[2]/div[4]/div[2]")[0].text_content().strip()
        counter+=1
        dataByIndex.append((Name,Platforms,VR,Release,Reviews,Discount,Price))
    except: break

#..
PD.set_option('display.max_columns', None) # momentary set for session to show all columns
#..
# Generating DataFrame
tabular=PD.DataFrame(dataByIndex,columns=column_list)
# printing DataFrame
print(tabular) 