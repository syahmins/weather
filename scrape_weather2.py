import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime # Ensure datetime is imported for datetime.now().date()

# 1. Define the API endpoint and parameters
# The provided URL already contains all necessary parameters
api_url = "https://api.open-meteo.com/v1/forecast?latitude=5.54829&longitude=95.323753&daily=temperature_2m_max,temperature_2m_min,uv_index_max,temperature_2m_mean&timezone=Asia%2FBangkok&past_days=31"

# 2. Fetch the data from the API
try:
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit() # Exit if data cannot be fetched

# 3. Extract relevant data for plotting
# The 'daily' key contains the arrays we need
daily_data = data.get('daily', {})

# Extract time and convert to datetime objects for proper plotting
time = pd.to_datetime(daily_data.get('time', []))
temperature_max = daily_data.get('temperature_2m_max', [])
temperature_min = daily_data.get('temperature_2m_min', [])
temperature_mean = daily_data.get('temperature_2m_mean', [])

# 4. Filter data to exclude future dates (forecast)
# Define the cutoff date as today's date
cutoff_date = pd.to_datetime(datetime.now().date())

# Create a boolean mask to select data up to and including the cutoff date
historical_mask = time <= cutoff_date

# Apply the mask to all data series
time_filtered = time[historical_mask]
temperature_max_filtered = [temperature_max[i] for i, is_historical in enumerate(historical_mask) if is_historical]
temperature_min_filtered = [temperature_min[i] for i, is_historical in enumerate(historical_mask) if is_historical]
temperature_mean_filtered = [temperature_mean[i] for i, is_historical in enumerate(historical_mask) if is_historical]


# 5. Create visualizations - now only one subplot for temperature, showing only historical data
fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(14, 7)) # Adjusted for single plot
# Updated title to reflect dynamic cutoff
fig.suptitle(f'30 Days Historical Weather Temperature (Up to {cutoff_date.strftime("%Y-%m-%d")})', fontsize=16)

# Plot temperatures on the single subplot using filtered data
ax1.plot(time_filtered, temperature_max_filtered, label='Max Temperature (°C)', color='red', marker='o', markersize=4, linestyle='-')
ax1.plot(time_filtered, temperature_min_filtered, label='Min Temperature (°C)', color='blue', marker='o', markersize=4, linestyle='-')
# ax1.plot(time_filtered, temperature_mean_filtered, label='Mean Temperature (°C)', color='green', marker='o', markersize=4, linestyle='--')
ax1.set_ylabel('Temperature (°C)', fontsize=12)
ax1.set_title('Daily Temperatures', fontsize=14)
ax1.set_xlabel('Date', fontsize=12) # Added xlabel to the single plot
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.7)

# Format the x-axis to display dates nicely
# Use a DateFormatter to show month and day
formatter = mdates.DateFormatter('%Y-%m-%d')
ax1.xaxis.set_major_formatter(formatter) # Apply formatter to the single plot
# Rotate date labels for better readability
plt.xticks(rotation=45, ha='right')


# 6. Add labels for highest, lowest temperatures, and today's temperature

if time_filtered.empty:
    print("No data available to plot labels.")
else:
    # Highest Temperature Annotation
    max_temp_val = max(temperature_max_filtered)
    # Corrected: Access element directly from DatetimeIndex
    max_temp_date = time_filtered[temperature_max_filtered.index(max_temp_val)]
    ax1.annotate(f'Highest: {max_temp_val:.1f}°C',
                 xy=(max_temp_date, max_temp_val),
                 xytext=(max_temp_date + pd.Timedelta(days=1), max_temp_val + 0.5), # Offset text for clarity
                 arrowprops=dict(facecolor='black', shrink=0.05, width=0.5, headwidth=5),
                 fontsize=9, color='red')

    # Lowest Temperature Annotation
    min_temp_val = min(temperature_min_filtered)
    # Corrected: Access element directly from DatetimeIndex
    min_temp_date = time_filtered[temperature_min_filtered.index(min_temp_val)]
    ax1.annotate(f'Lowest: {min_temp_val:.1f}°C',
                 xy=(min_temp_date, min_temp_val),
                 xytext=(min_temp_date + pd.Timedelta(days=1), min_temp_val - 0.5), # Offset text for clarity
                 arrowprops=dict(facecolor='black', shrink=0.05, width=0.5, headwidth=5),
                 fontsize=9, color='blue')

    # Today's Temperature Annotations (last data point in filtered lists)
    # Corrected: Access last element directly from DatetimeIndex
    today_date = time_filtered[-1]
    today_max_temp = temperature_max_filtered[-1]
    today_min_temp = temperature_min_filtered[-1]
    today_mean_temp = temperature_mean_filtered[-1]

    ax1.annotate(f'{today_max_temp:.1f}°C',
                 xy=(today_date, today_max_temp),
                 xytext=(today_date - pd.Timedelta(days=0), today_max_temp + 0.5),
                 # arrowprops=dict(facecolor='gray', shrink=0.05, width=0.5, headwidth=5),
                 fontsize=9, color='darkred')

    ax1.annotate(f'{today_min_temp:.1f}°C',
                 xy=(today_date, today_min_temp),
                 xytext=(today_date - pd.Timedelta(days=0), today_min_temp - 0.5),
                 # arrowprops=dict(facecolor='gray', shrink=0.05, width=0.5, headwidth=5),
                 fontsize=9, color='darkblue')
'''
    ax1.annotate(f'Today Mean: {today_mean_temp:.1f}°C',
                 xy=(today_date, today_mean_temp),
                 xytext=(today_date - pd.Timedelta(days=5), today_mean_temp + 0.5),
                 arrowprops=dict(facecolor='gray', shrink=0.05, width=0.5, headwidth=5),
                 fontsize=9, color='darkgreen')
'''
plt.tight_layout(rect=[0, 0.03, 1, 0.96]) # Adjust layout to prevent title overlap
plt.show()
