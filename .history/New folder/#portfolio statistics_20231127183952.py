#portfolio statistics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

#Open csv
df = pd.open_csv('historicalportfoliovalues_11_27_2023.csv', index_col='Date', parse_dates=True)