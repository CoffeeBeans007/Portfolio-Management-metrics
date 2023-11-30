import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=PF_Ref_df.index, y=PF_Ref_df["Total_Returns"], name="PF Ref"))
fig.add_trace(go.Scatter(x=sp_returns.index, y=sp_returns, name="S&P500"))
fig.add_trace(go.Scatter(x=returnss.index, y=returnss*100, name="PF"))

fig.update_layout(title="Portfolio Returns",
                  xaxis_title="Date",
                  yaxis_title="Returns")

fig.show()