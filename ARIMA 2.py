import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import itertools
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

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

    # Visualizing Stock Out Time Series Data
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
    results_dict = []

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y, order=param, seasonal_order=param_seasonal,
                                                enforce_stationarity=False, enforce_invertibility=False)
                results = mod.fit(disp=False)
                aic = results.aic
                results_dict.append((param, param_seasonal, aic, results))
            except:
                continue

    # Sort models by AIC
    results_dict = sorted(results_dict, key=lambda x: x[2])[:5]

    # Calculate RMSE, MAE, MAPE for top 5 models
    metrics = []
    models = [f'ARIMA{param}x{param_seasonal}12' for param, param_seasonal, aic, results in results_dict]
    aic_values = [aic for param, param_seasonal, aic, results in results_dict]

    for param, param_seasonal, aic, results in results_dict:
        pred = results.get_prediction(start=pd.to_datetime('2023-01-01'), dynamic=False)
        forecasted_mean = pred.predicted_mean
        actual_values = y['2023-01-01':]
        rmse = np.sqrt(mean_squared_error(actual_values, forecasted_mean))
        mae = mean_absolute_error(actual_values, forecasted_mean)
        mape = mean_absolute_percentage_error(actual_values, forecasted_mean) * 100
        metrics.append((rmse, mae, mape))

    # Create DataFrame for plotting
    metrics_df = pd.DataFrame(metrics, columns=['RMSE', 'MAE', 'MAPE'], index=models)

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    metrics_df.plot(kind='bar', ax=axes[0], color=['skyblue', 'lightgreen', 'salmon'], title='RMSE, MAE, MAPE of Top 5 ARIMA Models')
    axes[0].set_xlabel('Models')
    axes[0].set_ylabel('Metrics')
    axes[0].tick_params(axis='x', rotation=1, labelsize=8)
    axes[0].legend(['RMSE', 'MAE', 'MAPE'])

    aic_values_df = pd.Series(aic_values, index=models)
    aic_values_df.plot(kind='bar', ax=axes[1], color='lightblue', title='AIC Values of Top 5 ARIMA Models')
    axes[1].set_xlabel('Models')
    axes[1].set_ylabel('AIC')
    axes[1].tick_params(axis='x', rotation=1, labelsize=8)

    plt.tight_layout()
    plt.show()

    # ACF and PACF for the best model
    best_param, best_param_seasonal, best_aic, best_results = results_dict[0]
    y.dropna(inplace=True)

    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    plot_acf(y, ax=axes[0], lags=30, title='ACF of Best Model')
    axes[0].set_xlabel('Lags')
    axes[0].set_ylabel('ACF')
    plot_pacf(y, ax=axes[1], lags=30, title='PACF of Best Model')
    axes[1].set_xlabel('Lags')
    axes[1].set_ylabel('PACF')

    plt.tight_layout()
    plt.show()

    # Run model diagnostics for the best model
    best_results.plot_diagnostics(figsize=(15, 8))
    plt.show()

    # Validating forecasts of the best model
    pred_best = best_results.get_prediction(start=pd.to_datetime('2023-01-01'), dynamic=False)
    pred_ci_best = pred_best.conf_int()
    ax = y['2019':].plot(label='Observed')
    pred_best.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(12, 8))
    ax.fill_between(pred_ci_best.index, pred_ci_best.iloc[:, 0], pred_ci_best.iloc[:, 1], color='k', alpha=.2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Stock Out')
    plt.legend()
    plt.show()

    # Forecasting for 2024
    forecast_periods = 12
    forecast_index = pd.date_range(start=y.index[-1] + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
    forecast = best_results.get_forecast(steps=forecast_periods)
    forecast_mean = forecast.predicted_mean
    forecast_ci = forecast.conf_int()

    # Plotting the forecast for 2024
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
drug_combobox = ttk.Combobox(root, values=drugs, font=("Helvetica", 12))
drug_combobox.place(x=650, y=200)
drug_combobox.set("Select a drug")

# Add generate graphs button
generate_button = ttk.Button(root, text="Generate Graphs", command=generate_graphs, style="Generate.TButton")
generate_button.place(x=550, y=280)

# Add export to excel button
export_button = ttk.Button(root, text="Export to Excel", command=export_to_excel, style="Export.TButton")
export_button.place(x=750, y=280)

# Define custom style for buttons
style = ttk.Style()
style.configure("Generate.TButton", background="blue", foreground="black", height=3, font=("None", 12, "bold"), width=18)
style.configure("Export.TButton", background="blue", foreground="black", height=3, font=("None", 12, "bold"), width=18)

# Run the GUI
root.mainloop()
