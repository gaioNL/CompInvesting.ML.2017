#get data from Morningstar & store them in a file
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime

start = datetime(2013, 6, 5)
end = datetime(2013, 7, 15)

# Define the instruments to download.
tickers = ['VWRL.AS']

f = web.DataReader(tickers, 'morningstar', start, end)

f.head()

f.to_csv('%s.csv' % (tickers))