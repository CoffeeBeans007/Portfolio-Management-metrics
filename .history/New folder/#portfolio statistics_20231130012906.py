#portfolio statistics
import numpy as np
import pandas as pd
import plotly
import datetime as dt
import yfinance as yf
from sklearn.linear_model import LinearRegression
import sklearn
import matplotlib.pyplot as plt
from scipy import correlate
import statsmodels.api as sm
#Open csv
df = pd.read_csv('New folder\portfolio.csv', index_col='Date', parse_dates=True)


#Return beta of returns vs S&P500
returns = df.pct_change()
returns= returns["Value"]
returnss=returns
sp_returns = yf.download('^GSPC', start='2023-09-07', end='2023-11-23', progress=False)['Adj Close'].pct_change()

ReturnSPTSX = yf.download('^GSPTSE', start='2023-09-07', end='2023-11-23', progress=False)['Adj Close'].pct_change()
print(np.sum(ReturnSPTSX))
ReturnsXSPCad = yf.download('XSP.TO', start='2023-09-07', end='2023-11-23', progress=False)['Adj Close'].pct_change()
print(np.sum(ReturnsXSPCad))
ReturnsXINCad = yf.download('XIN.TO', start='2023-09-07', end='2023-11-23', progress=False)['Adj Close'].pct_change()
print(np.sum(ReturnsXINCad))

ReturnsaLT = 0.0933*(54/252)
print(ReturnsaLT)
ReturnsXBB = yf.download('XBB.TO', start='2023-09-07', end='2023-11-23', progress=False)['Adj Close'].pct_change()
print(np.sum(ReturnsXBB))

#Dataframe of returns

returns = pd.DataFrame(index=["CAN", "US", "INT", "ALT", "OB"], columns=["Returns"])
returns["Returns"] = [np.sum(ReturnSPTSX), np.sum(sp_returns), np.sum(ReturnsXINCad), ReturnsaLT, np.sum(ReturnsXBB)]
print(returns)

# Stdev sp returns
sp_returns_std = np.std(sp_returns)
print("S&P500 Standard Deviation: ", sp_returns_std)

#Display all stats
print("Slope: ", slope)
print("Intercept: ", intercept)
print("R Value: ", r_value)
print("P Value: ", p_value)
print("Standard Error: ", std_err)

#Regress returns of portfolio vs returns of S&P500
beta= np.cov(list(returns)[1:], list(sp_returns)[1:])[0,1]/np.var(sp_returns)
print("Beta: ", beta)

riskfree_ratea=0.0502/4
Jensen_alpha = 0.0708 - riskfree_ratea - beta*((0.0269)-riskfree_ratea)
print("Jensen Alpha: ", Jensen_alpha)

portfolio_returns= 0.0977

sharpe_ratio = np.mean(returns-sp_returns)/np.std(returns-sp_returns)

print("Sharpe Ratio: ", sharpe_ratio)

treynor_ratio = (0.0977-riskfree_ratea)/beta
print("Treynor Ratio: ", treynor_ratio)

