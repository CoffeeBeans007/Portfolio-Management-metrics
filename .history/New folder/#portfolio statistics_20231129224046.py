#portfolio statistics
import numpy as np
import pandas as pd
import plotly
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

#Regress returns of portfolio vs returns of S&P500
beta= np.cov(list(returns)[1:], list(sp_returns)[1:])[0,1]/np.var(sp_returns)
print("Beta: ", beta)

riskfree_ratea=0.0502/4
Jensen_alpha = 0.0708 - riskfree_ratea - beta*((0.0269)-riskfree_ratea)
print("Jensen Alpha: ", Jensen_alpha)

treynor_ratio = (0.0977-riskfree_ratea)/beta
print("Treynor Ratio: ", treynor_ratio)