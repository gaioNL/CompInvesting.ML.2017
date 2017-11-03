'''
@author: Gaio
@summary: read Yahoo historical prices with pyspark & play with data
'''

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime
import urllib2
import csv

#Gaio: pyspark imports
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext 

print "Pandas Version", pd.__version__

YAHOO_TODAY="http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=sd1ohgl1vl1"

def main():
    ''' Main Function'''

    conf = SparkConf().setAppName("yo yo")
    sc = SparkContext(conf=conf)
    sqlCtx = SQLContext(sc)       
    
    stocks = ['ORCL', 'TSLA', 'IBM','YELP', 'MSFT']
    ls_key = 'Adj Close'
    start = dt.datetime(2010, 12, 1)
    end = dt.datetime(2010, 12, 31)   
    f = web.DataReader(stocks, 'yahoo',start,end)
    
    cleanData = f.ix[ls_key]
    dataFrame = pd.DataFrame(cleanData)
    
    dataFrame = dataFrame.fillna(method='ffill')
    dataFrame = dataFrame.fillna(method='bfill')
    dataFrame = dataFrame.fillna(1.0)
        
    ldt_timestamps = dataFrame.index
    print 'TIMESTAMPS\n',ldt_timestamps    
    
    print 'PANDAS DF\n',dataFrame
    dataFrame_norm = dataFrame/dataFrame.iloc[0]
    print 'NORMALIZED PANDAS DF\n',dataFrame_norm
    
    df_price = sqlCtx.createDataFrame(dataFrame) 

    df_1st_row = df_price.limit(1)
    
    print '1st LINE SPARK DF\n',df_1st_row.show()
    
    exprs = [(df_price[x] / df_1st_row[x]) for x in df_1st_row.columns]

    df_norm = df_price.select(exprs)
    
    print 'PYSPARK DF\n', df_norm.show()

if __name__ == '__main__':
    main()