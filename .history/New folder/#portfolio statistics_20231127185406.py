#portfolio statistics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
#Open csv
df = pd.read_csv('New folder\portfolio.csv', index_col='Date', parse_dates=True)
print(df)

#Return beta of returns vs S&P500
returns = df.pct_change()

sp_returns = yf.download('^GSPC', start='2019-01-01', end='2021-01-01', progress=False)['Adj Close'].pct_change()
