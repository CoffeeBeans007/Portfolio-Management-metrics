#portfolio statistics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

#Open csv
df = pd.read_csv('portfolio.csv', index_col='Date', parse_dates=True)