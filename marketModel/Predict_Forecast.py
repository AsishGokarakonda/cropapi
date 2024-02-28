import pickle
import pandas as pd
import pmdarima as pm
import matplotlib.pyplot as plt

# Import Model from path
with open('marketModel/smodel(6,1,2)(0,1,1)[12].pkl', 'rb') as f:
    smodel = pickle.load(f)

# Path of data for the model area wise
dharwad         = 'marketModel/Dharwad_Price.txt'
hubbali         = 'marketModel/Hubbali_Price.txt'
vijayanagara    = 'marketModel/Vijayanagara_Price.txt'
udupi           = 'marketModel/Udupi_Price.txt'
bengaluru       = 'marketModel/Bengaluru_Price.txt'

# Area wise Data frames 
# dharwad_df      = pd.read_csv(dharwad)
# hubbali_df      = pd.read_csv(hubbali)
# vijayanagara_df = pd.read_csv(vijayanagara)
# udupi_df        = pd.read_csv(udupi)
# bengaluru_df    = pd.read_csv(bengaluru)

# Area Wise Data parsing
dharwad_data        = pd.read_csv(dharwad, parse_dates=['date'], index_col='date')
hubbali_data        = pd.read_csv(hubbali, parse_dates=['date'], index_col='date')
vijayanagara_data   = pd.read_csv(vijayanagara, parse_dates=['date'], index_col='date')
udupi_data          = pd.read_csv(udupi, parse_dates=['date'], index_col='date')
bengaluru_data      = pd.read_csv(bengaluru, parse_dates=['date'], index_col='date')



# Forecast (Enter number of months as n_periods)
n_periods = 6
last_n_months = 12
fitted, confint = smodel.predict(n_periods=n_periods, return_conf_int=True)


# Set indices of all the area wise datas
index_of_dharwad        = pd.date_range(dharwad_data.index[-1], periods=n_periods, freq='MS')
index_of_hubbali        = pd.date_range(hubbali_data.index[-1], periods=n_periods, freq='MS')
index_of_vijayanagara   = pd.date_range(vijayanagara_data.index[-1], periods=n_periods, freq='MS')
index_of_udupi          = pd.date_range(udupi_data.index[-1], periods=n_periods, freq='MS')
index_of_bengaluru      = pd.date_range(bengaluru_data.index[-1], periods=n_periods, freq='MS')


# make area-wise series for plotting purpose
dharwad_fitted_series   = pd.Series(fitted, index=index_of_dharwad)
dharwad_lower_series    = pd.Series(confint[:, 0], index=index_of_dharwad)
dharwad_upper_series    = pd.Series(confint[:, 1], index=index_of_dharwad)

# make area-wise series for plotting purpose
hubbali_fitted_series = pd.Series(fitted, index=index_of_hubbali)
hubbali_lower_series = pd.Series(confint[:, 0], index=index_of_hubbali)
hubbali_upper_series = pd.Series(confint[:, 1], index=index_of_hubbali)

# make area-wise series for plotting purpose
vijayanagara_fitted_series = pd.Series(fitted, index=index_of_vijayanagara)
vijayanagara_lower_series = pd.Series(confint[:, 0], index=index_of_vijayanagara)
vijayanagara_upper_series = pd.Series(confint[:, 1], index=index_of_vijayanagara)

# make area-wise series for plotting purpose
udupi_fitted_series = pd.Series(fitted, index=index_of_udupi)
udupi_lower_series = pd.Series(confint[:, 0], index=index_of_udupi)
udupi_upper_series = pd.Series(confint[:, 1], index=index_of_udupi)

# make area-wise series for plotting purpose
bengaluru_fitted_series = pd.Series(fitted, index=index_of_bengaluru)
bengaluru_lower_series = pd.Series(confint[:, 0], index=index_of_bengaluru)
bengaluru_upper_series = pd.Series(confint[:, 1], index=index_of_bengaluru)



# Print area-wise lower and upper confidence intervals
print("Dharwad Forecast:")
print(dharwad_lower_series)
print(dharwad_upper_series)

print("Hubbali Forecast:")
print(hubbali_lower_series)
print(hubbali_upper_series)

print("Vijayanagara Forecast:")
print(vijayanagara_lower_series)
print(vijayanagara_upper_series)

print("Udupi Forecast:")
print(udupi_lower_series)
print(udupi_upper_series)

print("Bengaluru Forecast:")
print(bengaluru_lower_series)
print(bengaluru_upper_series)


# 'data' is the full time series dataset and 'index_of_fc' is the index of forecast
# Slice the data to the last n months
last_n_months_dharwad         = dharwad_data[-last_n_months:]
last_n_months_hubbali         = hubbali_data[-last_n_months:]
last_n_months_vijayanagara    = vijayanagara_data[-last_n_months:]
last_n_months_udupi           = udupi_data[-last_n_months:]
last_n_months_bengaluru       = bengaluru_data[-last_n_months:]

# ----------------------------------------------------------------------------------------------------------------------
# Plot
plt.plot(last_n_months_dharwad, label='Observed')  # Plot the last 6 months of observed data
plt.plot(dharwad_fitted_series, color='darkgreen', label='Forecast')  # Plot the forecasted data
plt.fill_between(dharwad_lower_series.index, 
                 dharwad_lower_series, 
                 dharwad_upper_series, 
                 color='k', alpha=.15, label='Confidence Interval')

# Add titles and labels
plt.title("Dharwad: Final Forecast of Future Cotton Prices")
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Display the plot
plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# Plot
plt.plot(last_n_months_hubbali, label='Observed')  # Plot the last 6 months of observed data
plt.plot(hubbali_fitted_series, color='darkred', label='Forecast')  # Plot the forecasted data
plt.fill_between(hubbali_lower_series.index, 
                 hubbali_lower_series, 
                 hubbali_upper_series, 
                 color='k', alpha=.15, label='Confidence Interval')

# Add titles and labels
plt.title("Hubbali: Final Forecast of Future Cotton Prices")
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Display the plot
plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# Plot
plt.plot(last_n_months_vijayanagara, label='Observed')  # Plot the last 6 months of observed data
plt.plot(vijayanagara_fitted_series, color='darkgreen', label='Forecast')  # Plot the forecasted data
plt.fill_between(vijayanagara_lower_series.index, 
                 vijayanagara_lower_series, 
                 vijayanagara_upper_series, 
                 color='k', alpha=.15, label='Confidence Interval')

# Add titles and labels
plt.title("Vijayanagara: Final Forecast of Future Cotton Prices")
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Display the plot
plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# Plot
plt.plot(last_n_months_udupi, label='Observed')  # Plot the last 6 months of observed data
plt.plot(udupi_fitted_series, color='darkblue', label='Forecast')  # Plot the forecasted data
plt.fill_between(udupi_lower_series.index, 
                 udupi_lower_series, 
                 udupi_upper_series, 
                 color='k', alpha=.15, label='Confidence Interval')

# Add titles and labels
plt.title("Udupi: Final Forecast of Future Cotton Prices")
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Display the plot
plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# Plot
plt.plot(last_n_months_bengaluru, label='Observed')  # Plot the last 6 months of observed data
plt.plot(bengaluru_fitted_series, color='darkblue', label='Forecast')  # Plot the forecasted data
plt.fill_between(bengaluru_lower_series.index, 
                 bengaluru_lower_series, 
                 bengaluru_upper_series, 
                 color='k', alpha=.15, label='Confidence Interval')

# Add titles and labels
plt.title("Bengaluru: Final Forecast of Future Cotton Prices")
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Display the plot
plt.show()

# ----------------------------------------------------------------------------------------------------------------------
