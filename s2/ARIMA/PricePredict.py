import pickle
import pandas as pd
import pmdarima as pm
import matplotlib.pyplot as plt

MONTHS = 6

with open('smodel.pkl', 'rb') as f:
    model = pickle.load(f)
    
path = 'Price.txt'
df = pd.read_csv(path)
data = pd.read_csv(path, parse_dates=['date'], index_col='date')


n_periods = MONTHS
fitted, confint = model.predict(n_periods=n_periods, return_conf_int=True)
index_of_fc = pd.date_range(data.index[-1], periods = n_periods, freq='MS')

# make series for plotting purpose
fitted_series = pd.Series(fitted, index=index_of_fc)
lower_series = pd.Series(confint[:, 0], index=index_of_fc)
upper_series = pd.Series(confint[:, 1], index=index_of_fc)
print(lower_series)
print(upper_series)

# Plot
plt.plot(data)
plt.plot(fitted_series, color='darkgreen')
plt.fill_between(lower_series.index, 
                 lower_series, 
                 upper_series, 
                 color='k', alpha=.15)

plt.title("SARIMA - Final Forecast of Cotton Prices - Time Series Dataset")
plt.show()
