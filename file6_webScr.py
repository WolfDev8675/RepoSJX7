#!usr/bin/python

# Package structure for access over net for data files
# Net access using packages from Requests

import requests as rqs # rqs as requests.py alias 

def accessFile(source_url,dest_path,file_name):
      """ Function to access data file 
        Specific usage using the REQUESTS package ver 2.25.1
          source_url : to contain the source of file in the web
          dest_path  : to contain the path to a specific folder where the file is to be downloaded
          file_name  : to contain the save name of the file complete with extension """
      
      # accesing the content specific as to file
      file_cont=rqs.get(source_url).content
      
      # defining complete path to the destination
      c_path=dest_path+'\\'+file_name  
      
      # write to file
      with open(fr"{c_path}",'wb') as f_wr:
          f_wr.write(file_cont)     
      
      return c_path   # return path of file 

