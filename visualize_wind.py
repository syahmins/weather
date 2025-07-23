import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Your Open-Meteo API URL
api_url = "https://api.open-me" \
          "teo.com/v1/forecast?latitude=5.54829&longitude=95.323753&daily=wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant&timezone=Asia%2FBangkok&past_days=14"

# Fetch data from the API
try:
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from the API: {e}")
    exit()

# Extract relevant daily data
daily_data = data['daily']

# Create a DataFrame
df = pd.DataFrame({
    'date': pd.to_datetime(daily_data['time']),
    'max_wind_speed': daily_data['wind_speed_10m_max'],
    'max_wind_gust': daily_data['wind_gusts_10m_max']
})

# Set the date as the index
df = df.set_index('date')

# --- Create the Two-Row Line Graphs ---
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 8), sharex=True)

# Plot Max Wind Speed on the top subplot
axes[0].plot(df.index, df['max_wind_speed'], marker='o', linestyle='-', color='b')
axes[0].set_title('Daily Maximum Wind Speed (Last 14 Days)')
axes[0].set_ylabel('Speed (km/h)')
axes[0].grid(True, which='both', linestyle='--', linewidth=0.5)

# Plot Max Wind Gusts on the bottom subplot
axes[1].plot(df.index, df['max_wind_gust'], marker='o', linestyle='--', color='r')
axes[1].set_title('Daily Maximum Wind Gusts (Last 14 Days)')
axes[1].set_ylabel('Speed (km/h)')
axes[1].set_xlabel('Date')
axes[1].grid(True, which='both', linestyle='--', linewidth=0.5)

# Format the x-axis to show dates cleanly (shared by both plots)
axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
axes[1].xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.xticks(rotation=45, ha='right')

# Adjust layout for a clean appearance
plt.tight_layout()
plt.suptitle('Daily Wind Conditions in Banda Aceh', y=1.02, fontsize=16)
plt.show()

print("DataFrame used for plotting:")
print(df)