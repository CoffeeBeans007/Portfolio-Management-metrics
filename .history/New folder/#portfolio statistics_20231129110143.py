#portfolio statistics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
#Open csv
df = pd.read_csv('New folder\portfolio.csv', index_col='Date', parse_dates=True)


#Return beta of returns vs S&P500
returns = df.pct_change()
returns= returns["Value"]

sp_returns = yf.download('^GSPC', start='2023-09-07', end='2023-11-23', progress=False)['Adj Close'].pct_change()


#Match both returns on index
returns = returns[sp_returns.index]
print(sp_returns.shape)
print(returns.shape)
#Regress returns of portfolio vs returns of S&P500
beta= np.cov(returns, sp_returns)/np.var(sp_returns)
print(beta)