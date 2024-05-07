import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import itertools
import statsmodels.api as sm

# Suppress warnings
warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_excel("pharma_sales_dataset.xlsx")

# Create tkinter window
root = tk.Tk()
root.title("Pharma Sales Forecasting")

# Set initial window geometry
root.geometry("1350x750")

# Function to perform ARIMA forecasting and generate graphs
def generate_graphs():
    selected_drug = drug_combobox.get()
    drug_data = df[df['Drug'] == selected_drug]

    # Data Preprocessing
    drug_data['Date'] = pd.to_datetime(drug_data['Date'])
    drug_data.set_index('Date', inplace=True)
    y = drug_data['Stock Out'].resample('MS').mean() * 30

    # Visualizing Paracetamol Sales Time Series Data
    plt.figure(figsize=(15, 12))
    plt.plot(y)
    plt.title('Stock Out for ' + selected_drug)
    plt.xlabel('Date')
    plt.ylabel('Stock Out')
    plt.show()

    # Time-series decomposition method
    decomposition = sm.tsa.seasonal_decompose(y, model='additive', period=6)
    fig = decomposition.plot()
    plt.show()

    # Time series forecasting with ARIMA
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    # Parameter Selection for ARIMA model
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y, order=param, seasonal_order=param_seasonal,
                                                enforce_stationarity=False, enforce_invertibility=False)
                results = mod.fit()
                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue

    # Fitting the ARIMA model
    mod = sm.tsa.statespace.SARIMAX(y, order=(0, 0, 0), seasonal_order=(1, 1, 0, 12),
                                    enforce_stationarity=False, enforce_invertibility=False)
    results = mod.fit()

    # Run model diagnostics
    results.plot_diagnostics(figsize=(22, 20))
    plt.show()

    # Validating forecasts
    pred = results.get_prediction(start=pd.to_datetime('2023-01-01'), dynamic=False)
    pred_ci = pred.conf_int()
    ax = y['2019':].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(12, 8))
    ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='k', alpha=.2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Stock Out')
    plt.legend()
    plt.show()

    pred = results.get_prediction(start=pd.to_datetime('2023-01-01'), dynamic=False)
    forecasted_mean = pred.predicted_mean
    forecasted_ci = pred.conf_int()

    # Get actual values for the validation period
    actual_values = y['2023-01-01':]

    # Calculate Mean Absolute Deviation (MAD)
    mad = np.mean(np.abs(actual_values - forecasted_mean))

    # Calculate Mean Squared Error (MSE)
    mse = np.mean((actual_values - forecasted_mean) ** 2)

    # Calculate Mean Absolute Percentage Error (MAPE)
    mape = np.mean(np.abs((actual_values - forecasted_mean) / actual_values)) * 100

    # Print the metrics
    print("Mean Absolute Deviation (MAD):", mad)
    print("Mean Squared Error (MSE):", mse)
    print("Mean Absolute Percentage Error (MAPE):", mape)

    # Forecasting for 2024
    forecast_periods = 12
    forecast_index = pd.date_range(start=y.index[-1] + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
    forecast = results.get_forecast(steps=forecast_periods)
    forecast_mean = forecast.predicted_mean
    forecast_ci = forecast.conf_int()

    # Plotting the forecast
    ax = y.plot(label='Observed', figsize=(12, 8))
    forecast_mean.plot(ax=ax, label='Forecast', color='red')
    ax.fill_between(forecast_ci.index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='red', alpha=0.2)
    ax.axvspan(forecast_index[0], forecast_index[-1], alpha=0.1, color='gray')
    ax.set_xlabel('Date')
    ax.set_ylabel('Stock Out')
    plt.legend()
    plt.show()

    # Export forecasted data to Excel
    forecast_df = pd.DataFrame({'Date': forecast_index, 'Predicted_Stock_Out': forecast_mean,
                                'Lower_CI': forecast_ci.iloc[:, 0], 'Upper_CI': forecast_ci.iloc[:, 1]})
    forecast_df.to_excel('forecasted_stock_out.xlsx', index=False)

# Function to export forecasted data to Excel
def export_to_excel():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        forecast_df = pd.read_excel('forecasted_stock_out.xlsx')
        forecast_df.to_excel(file_path, index=False)

# Add dropdown for selecting drug
drug_label = ttk.Label(root, text="Select Drug:", font=("Helvetica", 12, "bold"))
drug_label.place(x=530, y=200)
drugs = df['Drug'].unique().tolist()
drug_combobox = ttk.Combobox(root, values=drugs, state="readonly", font=("Helvetica", 12, "bold"))
drug_combobox.current(0)
drug_combobox.place(x=650, y=200)

# Add button to generate graphs
generate_button = ttk.Button(root, text="Generate Graphs", command=generate_graphs, style="Generate.TButton")
generate_button.place(x=650, y=240)

# Add button to export forecasted data to Excel
export_button = ttk.Button(root, text="Export", command=export_to_excel, style="Export.TButton")
export_button.place(x=650, y=280)

# Define custom style for buttons
style = ttk.Style()
style.configure("Generate.TButton", background="blue", foreground="black", height=3, font=("None", 12, "bold"), width=18)
style.configure("Export.TButton", background="blue", foreground="black", height=3, font=("None", 12, "bold"), width=18)

# Run the GUI
root.mainloop()
