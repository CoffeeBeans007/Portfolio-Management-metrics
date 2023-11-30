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



returns = df.pct_change()
returns= returns["Value"]
returnss=returns

sp_returns = yf.download('^GSPC', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(sp_returns))
ReturnSPTSX = yf.download('^GSPTSE', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(ReturnSPTSX))
ReturnsXSPCad = yf.download('XSP.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(ReturnsXSPCad))
ReturnsXINCad = yf.download('XIN.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(ReturnsXINCad))

ReturnsaLT = yf.download('CMR.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(ReturnsaLT))
ReturnsXBB = yf.download('XBB.TO', start='2023-09-01', end='2023-11-21', progress=False)['Adj Close'].pct_change()*100
print(np.sum(ReturnsXBB))




#Calculating the returns of each asset class
returns = pd.DataFrame(index=["CAN", "US", "INT", "ALT", "OB"], columns=["Returns"])
returns["Returns"] = [np.sum(ReturnSPTSX), np.sum(sp_returns), np.sum(ReturnsXINCad), ReturnsaLT, np.sum(ReturnsXBB)]

#Constructing an evoluting portfolio of all 5 asset classes based on chosen weights   CAN  35%  US     20%  INT   10%  ALT  15%  OB    10%
PF_Ref = np.array([0.20 * ReturnSPTSX, 0.15 * ReturnsXSPCad, 0.15 * ReturnsXINCad, 0.40 * ReturnsaLT, 0.1 * ReturnsXBB])
PF_Ref_df= pd.DataFrame(columns=["CAN", "US", "INT", "ALT", "OB"],index=ReturnSPTSX.index)
PF_Ref_df["CAN"]= PF_Ref[0]
PF_Ref_df["US"]= PF_Ref[1]
PF_Ref_df["INT"]= PF_Ref[2]
PF_Ref_df["ALT"]= PF_Ref[3]
PF_Ref_df["OB"]= PF_Ref[4]
PF_Ref_df["Total_Returns"]= PF_Ref_df.sum(axis=1)
print(PF_Ref_df)

index_returns=np.array(PF_Ref_df["Total_Returns"])

PF_Ref_df["Total_Returns"]=returns

# Stdev PF returns
PF_Ref_std = np.std(PF_Ref_df["Total_Returns"])
print("PF Standard Deviation: ", PF_Ref_std)
# Stdev sp returns
index_returns_std = np.std(index_returns)
print("S&P500 Standard Deviation: ", index_returns_std)

#Value at risk at 95 percent confidence interval
historic_var = (np.percentile(PF_Ref_df["Total_Returns"], 5, interpolation="lower"))
print(f"Historic VaR($): {historic_var} Dollars")

#Beta of PF
Beta_PF = np.cov(PF_Ref_df["Total_Returns"], index_returns[2:])/np.var(sp_returns)
print("Beta of PF: ", Beta_PF)

#Risk free of 3 month T-bill brought back to 52 days (Simulation length)
riskfree_return=0.0527*52/254*100

# CAPM (Medaf) Expected Return of PF
ERB=riskfree_return+Beta_PF*(2.69-riskfree_return)
print("Expected Return of PF|Beta: ", ERB)
#Regress returns of portfolio vs returns of S&P500

#Replication Error
Replication_Error = np.std(PF_Ref_df["Total_Returns"]-sp_returns[1:])
print("Replication Error: ", Replication_Error)

#Information Ratio
IR = (np.sum(PF_Ref_df["Total_Returns"]-sp_returns[1:]))/Replication_Error
print("Information Ratio: ", IR)

Jensen_alpha = 0.0708 - riskfree_return + Beta_PF*((0.0269)*100-riskfree_return)
print("Jensen Alpha: ", Jensen_alpha)

portfolio_returns_stocktrack= 0.0977

treynor_ratio = (0.0977-riskfree_return/100)/Beta_PF
print("Treynor Ratio: ", treynor_ratio)


import plotly.graph_objects as go

cumulative_PF_Ref = (1 + PF_Ref_df["Total_Returns"]).cumprod() - 1
cumulative_sp_returns = sp_returns.cumsum()
cumulative_returnss = returnss.cumsum()

fig = go.Figure()
fig.add_trace(go.Scatter(x=PF_Ref_df.index, y=cumulative_PF_Ref, name="PF Ref"))
fig.add_trace(go.Scatter(x=sp_returns.index, y=cumulative_sp_returns, name="S&P500"))
fig.add_trace(go.Scatter(x=returnss.index, y=cumulative_returnss*100, name="PF"))

fig.update_layout(title="Cumulative Portfolio Returns",
                  xaxis_title="Date",
                  yaxis_title="Cumulative Returns")

fig.show()
