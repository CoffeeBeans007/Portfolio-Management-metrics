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

# Calculate returns
returns = df.pct_change()
returns = returns["Value"]
returnss = returns

# Download market data
sp_returns = yf.download('^GSPC', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change() * 100
ReturnSPTSX = yf.download('^GSPTSE', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change() * 100
ReturnsXSPCad = yf.download('XSP.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change() * 100
ReturnsXINCad = yf.download('XIN.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change() * 100
ReturnsaLT = yf.download('CMR.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change() * 100
ReturnsXBB = yf.download('XBB.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change() * 100

# Calculate returns of each asset class
returns = pd.DataFrame(index=["CAN", "US", "INT", "ALT", "OB"], columns=["Returns"])
returns["Returns"] = [np.sum(ReturnSPTSX), np.sum(sp_returns), np.sum(ReturnsXINCad), ReturnsaLT, np.sum(ReturnsXBB)]

# Constructing an evolving portfolio of all 5 asset classes based on chosen weights
PF_Ref = np.array([0.35 * ReturnSPTSX, 0.2 * sp_returns, 0.1 * ReturnsXINCad, 0.15 * ReturnsaLT, 0.1 * ReturnsXBB])
PF_Ref_df = pd.DataFrame(columns=["CAN", "US", "INT", "ALT", "OB"], index=ReturnSPTSX.index)
PF_Ref_df["CAN"] = PF_Ref[0]
PF_Ref_df["US"] = PF_Ref[1]
PF_Ref_df["INT"] = PF_Ref[2]
PF_Ref_df["ALT"] = PF_Ref[3]
PF_Ref_df["OB"] = PF_Ref[4]
PF_Ref_df["Total_Returns"] = PF_Ref_df.sum(axis=1)

# Calculate standard deviation of portfolio returns
PF_Ref_std = np.std(PF_Ref_df["Total_Returns"])

# Calculate standard deviation of S&P500 returns
sp_returns_std = np.std(sp_returns)

# Calculate historic Value at Risk at 95 percent confidence interval
historic_var = (np.percentile(PF_Ref_df["Total_Returns"], 5, interpolation="lower") / 100) * 500000

# Calculate Beta of the portfolio
Beta_PF = np.cov(PF_Ref_df["Total_Returns"], sp_returns[1:])[0, 1] / np.var(sp_returns)

# Calculate risk-free return
riskfree_return = 0.0527 * 52 / 254 * 100

# Calculate Expected Return of the portfolio using CAPM (Medaf)
ERB = riskfree_return + Beta_PF * (2.69 - riskfree_return)

# Calculate Replication Error
Replication_Error = np.std(PF_Ref_df["Total_Returns"] - sp_returns[1:])

# Calculate Information Ratio
IR = (np.sum(PF_Ref_df["Total_Returns"] - sp_returns[1:])) / Replication_Error

# Calculate Jensen Alpha
Jensen_alpha = 0.0708 - riskfree_return + Beta_PF * ((0.0269) * 100 - riskfree_return)

# Calculate Treynor Ratio
portfolio_returns_stocktrack = 0.0977
treynor_ratio = (0.0977 - riskfree_return / 100) / Beta_PF

import plotly.graph_objects as go
# Calculate cumulative returns
cumulative_PF_Ref = (1 + PF_Ref_df["Total_Returns"]).cumprod() - 1
cumulative_sp_returns = sp_returns.cumsum()
cumulative_returnss = returnss.cumsum()

# Plot cumulative portfolio returns
fig = go.Figure()
fig.add_trace(go.Scatter(x=PF_Ref_df.index, y=cumulative_PF_Ref, name="PF Ref"))
fig.add_trace(go.Scatter(x=sp_returns.index, y=cumulative_sp_returns, name="S&P500"))
fig.add_trace(go.Scatter(x=returnss.index, y=cumulative_returnss * 100, name="PF"))

fig.update_layout(title="Cumulative Portfolio Returns",
                  xaxis_title="Date",
                  yaxis_title="Cumulative Returns")

fig.show()
