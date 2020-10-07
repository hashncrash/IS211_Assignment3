#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 Week 3 Assignment
Dave Soto"""



import urllib.request
from io import StringIO
import csv
import re #regular expression
import argparse
import datetime

# Part 1
def downloadData(url):
    """function to download the contents of the csv file"""
    content=urllib.request.urlopen(url).read().decode("ascii","ignore") 
    return content

# Part 2
def processData(file):
    """Funtion to do a line by line process of the fie"""
    data=StringIO(file)
    csv_reader = csv.reader(data, delimiter=',')
    next(csv_reader)
    dataList=[] 
    for line in csv_reader:
        dataList.append(line)
    return dataList

imageBroswerList=[] 

#part 3
def imageHits(dataList):
    """Function to search forthe image file"""
    count=0 
    imageCount=0 
    
    for line in dataList: 
        extensionList=re.findall('([^\s]+(\.(?i)(jpg|png|gif|bmp))$)',line[0]) 
        
        if len(extensionList)>0: 
            imageCount+=1 
            imageBroswerList.append(line)
            
        count+=1 
    
    imagePercentage=(imageCount/count)* 100  
    imagePercentage=round(imagePercentage,1) 
    print("Image requests account for {} % of all requests".format(imagePercentage))

#part 4
def browserType(imageBroswerList=imageBroswerList):
    """Function for finding the popular browser"""
    browserCounts={}  

    browserList=[]  
    for line in imageBroswerList:
        browserType=re.findall("(?i)(firefox|msie|chrome|safari)[/\s]([\d.]+)", line[2]) 
        
        browserList.append(browserType) 
    for broswers in browserList:
        if broswers[0][0] not in browserCounts:
            browserCounts[broswers[0][0]]=1
        else:
            browserCounts[broswers[0][0]]+=1 
    
    browserTup=list() 
    for key, value in list(browserCounts.items()):
        browserTup.append((value,key))
    
    browserTup.sort(reverse=True) 

    print("The most popular browser is {} with {} hits".format(browserTup[0][1], browserTup[0][0]))

#Extra credit
def hourHits(dataList):

    hitsDict={}
    for data in dataList:
        hours= datetime.datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S').hour #extract hours from date time
        if hours not in hitsDict:
            hitsDict[hours]=1
        else:
            hitsDict[hours]+=1

    hitsTup=list() 
    for key, value in list(hitsDict.items()):
        hitsTup.append((value,key)) 
    
    hitsTup.sort(reverse=True) 
    for i,value in hitsTup:
        print("Hour {} has {} hits".format(value, i)) 


 
def main():
    commandParser = argparse.ArgumentParser(description="Send a ­­url parameter to the script")
    commandParser.add_argument("--url", type=str, help="Link to the csv file")
    args = commandParser.parse_args()
    if not args.url:
        exit()
    
    
    try:
        csvData=downloadData(args.url)
    except:
        print("An error has occured. Please try again")
        exit()
    browserData=processData(csvData)
    image=imageHits(browserData)
    browserType()
    hourHits(browserData)

if __name__ == "__main__":
    main()


