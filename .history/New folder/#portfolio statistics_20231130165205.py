"""
This script calculates various portfolio statistics based on the provided data.
"""

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

# Open csv
df = pd.read_csv('New folder\portfolio.csv', index_col='Date', parse_dates=True)

# Calculate daily returns
returns = df.pct_change()
returns = returns["Value"]
print(returns)
returnss = returns.values

# Download S&P 500 returns
sp_returns = yf.download('^GSPC', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(sp_returns))

# Download S&P/TSX Composite Index returns
ReturnSPTSX = yf.download('^GSPTSE', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(ReturnSPTSX))

# Download XSP.TO returns
ReturnsXSPCad = yf.download('XSP.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(ReturnsXSPCad))

# Download XIN.TO returns
ReturnsXINCad = yf.download('XIN.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(ReturnsXINCad))

# Download CMR.TO returns
ReturnsaLT = yf.download('CMR.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(ReturnsaLT))

# Download XBB.TO returns
ReturnsXBB = yf.download('XBB.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(ReturnsXBB))

# Constructing an evolving portfolio of all 5 asset classes based on chosen weights
# CAN 35%, US 20%, INT 10%, ALT 15%, OB 10%
PF_Ref = np.array([0.20 * ReturnSPTSX, 0.15 * ReturnsXSPCad, 0.15 * ReturnsXINCad, 0.40 * ReturnsaLT, 0.1 * ReturnsXBB])
PF_Ref_df = pd.DataFrame(columns=["CAN", "US", "INT", "ALT", "OB"], index=ReturnSPTSX.index)
PF_Ref_df["CAN"] = PF_Ref[0]
PF_Ref_df["US"] = PF_Ref[1]
PF_Ref_df["INT"] = PF_Ref[2]
PF_Ref_df["ALT"] = PF_Ref[3]
PF_Ref_df["OB"] = PF_Ref[4]
PF_Ref_df["Total_Returns"] = PF_Ref_df.sum(axis=1)
print(PF_Ref_df)

index_returns = np.array(PF_Ref_df["Total_Returns"])
index_return_total = np.sum(index_returns)

Portfolio_Returns = returns

# Remove weekends from Portfolio_Returns
Portfolio_Returns = Portfolio_Returns[Portfolio_Returns.index.dayofweek < 5]

# Calculate standard deviation of portfolio returns
PF_Ref_std = np.std(Portfolio_Returns)*100
print("PF Standard Deviation: ", PF_Ref_std)

# Calculate standard deviation of S&P 500 returns
index_returns_std = np.std(index_returns)
print("S&P500 Standard Deviation: ", index_returns_std)

# Calculate historic Value at Risk at 95 percent confidence interval
Portfolio_Returns = np.nan_to_num(Portfolio_Returns, 0)
historic_var = np.percentile(Portfolio_Returns, 5)*500000
print(f"Historic VaR($): {historic_var} Dollars")

# Convert portfolio returns to percentage
Portfolio_Returns = Portfolio_Returns*100

# Calculate Beta of the portfolio
Beta_PF = np.cov(Portfolio_Returns, index_returns)[0, 1] / np.var(index_returns)
print("Beta of PF: ", Beta_PF)

# Calculate risk-free return
riskfree_return = 0.0527 * 52 / 254 * 100

# Calculate Expected Return of the portfolio using CAPM (Medaf)
ERB = riskfree_return + Beta_PF * (index_return_total - riskfree_return)
print("Expected Return of PF|Beta: ", ERB)

# Calculate Replication Error
Replication_Error = (PF_Ref_std - index_returns_std)
print("Replication Error: ", Replication_Error)

# Calculate Information Ratio
IR = (np.sum(Portfolio_Returns - index_returns)) / (Replication_Error * 100)
print("Information Ratio: ", IR)

# Calculate Jensen Alpha
alpha = np.sum(Portfolio_Returns) / 100 - np.sum(index_returns)
Jensen_alpha = alpha - riskfree_return + Beta_PF * ((index_return_total) * 100 - riskfree_return)
print(alpha)
print("Jensen Alpha: ", Jensen_alpha / 100)

portfolio_returns_stocktrack = 0.0977

# Calculate Treynor Ratio
treynor_ratio = (0.0977 - riskfree_return / 100) / Beta_PF
print("Treynor Ratio: ", treynor_ratio)
