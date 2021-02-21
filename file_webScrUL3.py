#!usr/bin/python

# Package structure for access over net for data files
# Net access using packages from Requests

import urllib3 as netr # netr as urllib3.py alias 

def accessFile(source_url,dest_path,file_name):
      """ Function to access data file 
        Specific usage using the URLLIB3 package ver 1.26.3
          source_url : to contain the source of file in the web
          dest_path  : to contain the path to a specific folder where the file is to be downloaded
          file_name  : to contain the save name of the file complete with extension """
      
      # initializing pool manager
      poolM= netr.PoolManager()
      
      # accesing the content specific as to file from url response request
      file_cont = poolM.request('GET', source_url).data

      # defining complete path to the destination
      c_path=dest_path+'\\'+file_name  

      # write to file 
      with open(fr"{c_path}",'wb') as f_wr:
          f_wr.write(file_cont)    
      
      return c_path   # return path of file 
#end of function

#end of code
      
