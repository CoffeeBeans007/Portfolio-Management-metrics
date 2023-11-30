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
print(returns)
returnss=returns.values


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

Portfolio_Returns=returns
print(Portfolio_Returns*100)
Portfolio_Returns = Portfolio_Returns[Portfolio_Returns.index.isin(index_returns)]

print("hello")
print(np.array(Portfolio_Returns))
print("hello")

# Stdev PF returns
PF_Ref_std = np.std(Portfolio_Returns)
print("PF Standard Deviation: ", PF_Ref_std*100)
# Stdev sp returns
index_returns_std = np.std(index_returns)
print("S&P500 Standard Deviation: ", index_returns_std)

#Value at risk at 95 percent confidence interval
print(PF_Ref_df["Total_Returns"])

historic_var = np.percentile(Portfolio_Returns, 5)*500000
print(f"Historic VaR($): {historic_var} Dollars")

#Add missing days to index returns

Beta_PF = np.cov(Portfolio_Returns, index_returns)[0, 1] / np.var(index_returns)
print("Beta of PF: ", Beta_PF)

#Risk free of 3 month T-bill brought back to 52 days (Simulation length)
riskfree_return = 0.0527 * 52 / 254 * 100

# CAPM (Medaf) Expected Return of PF
ERB=riskfree_return+Beta_PF*(2.69-riskfree_return)
print("Expected Return of PF|Beta: ", ERB)
#Regress returns of portfolio vs returns of S&P500

#Replication Error
Replication_Error = np.std(PF_Ref_df["Total_Returns"]-index_returns)
print("Replication Error: ", Replication_Error)

#Information Ratio
IR = (np.sum(PF_Ref_df["Total_Returns"]-index_returns))/Replication_Error
print("Information Ratio: ", IR)

Jensen_alpha = 0.0708 - riskfree_return + Beta_PF*((0.0269)*100-riskfree_return)
print("Jensen Alpha: ", Jensen_alpha)

portfolio_returns_stocktrack= 0.0977

treynor_ratio = (0.0977-riskfree_return/100)/Beta_PF
print("Treynor Ratio: ", treynor_ratio)



