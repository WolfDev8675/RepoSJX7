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
colData=dict.fromkeys(column_list,[])

# HTML Tree Generation
plants=HT.fromstring(data) 
counter=1 #primary value 
try:
    colData["Name"].append(plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div/div[3]/a["+str(counter)+"]/div[2]/div[1]/span")[0].text_content())
    colData["Platforms"].append(plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div[2]/div[3]/a["+str(counter)+"]/div[2]/div[1]/p/span[1]")[0].text_content())
    colData["VR"].append(plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div[2]/div[3]/a[1]/div[2]/div[1]/p/span[2]")[0].text_content())
    colData["Release"].append(plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div[2]/div[3]/a[3]/div[2]/div[2]")[0].text_content())
    colData["Reviews"].append(str(list(plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div[2]/div[3]/a["+str(counter)+"]/div[2]/div[3]/span")[0].values())[0]).split()[1])
    colData["Discount"].append(plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div[2]/div[3]/a["+str(counter)+"]/div[2]/div[4]/div[1]/span")[0].text_content().strip())
    colData["Price"].append(plants.xpath("/html/body/div[1]/div[7]/div[4]/form/div[1]/div/div[1]/div[3]/div/div[3]/a["+str(counter)+"]/div[2]/div[4]/div[2]")[0].text_content().strip())
except:
    pass 
