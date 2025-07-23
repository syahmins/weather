import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

'''
Configuration
Set the location and time period for data fetching.
Modify this section to localize the data.
'''
LATITUDE = 5.54829
LONGITUDE = 95.323753
PAST_DAYS = 14
TIMEZONE = "Asia/Bangkok"

# --- Beaufort Scale Conversion Function ---
def convert_to_beaufort(speed_kmh):
    """Converts wind speed (in km/h) to its corresponding Beaufort Scale value."""
    if speed_kmh < 1: return 0
    elif 1 <= speed_kmh <= 5: return 1
    elif 6 <= speed_kmh <= 11: return 2
    elif 12 <= speed_kmh <= 19: return 3
    elif 20 <= speed_kmh <= 29: return 4
    elif 30 <= speed_kmh <= 39: return 5
    elif 40 <= speed_kmh <= 50: return 6
    elif 51 <= speed_kmh <= 61: return 7
    elif 62 <= speed_kmh <= 74: return 8
    elif 75 <= speed_kmh <= 87: return 9
    elif 88 <= speed_kmh <= 101: return 10
    elif 102 <= speed_kmh <= 117: return 11
    else: return 12

# --- Data Fetching and Processing ---
api_url = (
    f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&"
    f"daily=wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant&"
    f"timezone={TIMEZONE}&past_days={PAST_DAYS}"
)

try:
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from the API: {e}")
    exit()

daily_data = data['daily']

df = pd.DataFrame({
    'date': pd.to_datetime(daily_data['time']),
    'max_wind_speed': daily_data['wind_speed_10m_max'],
    'max_wind_gust': daily_data['wind_gusts_10m_max']
})

# --- Conversion to Beaufort Scale ---
df['beaufort_wind_speed'] = df['max_wind_speed'].apply(convert_to_beaufort)
df['beaufort_wind_gust'] = df['max_wind_gust'].apply(convert_to_beaufort)

df = df.set_index('date')

# --- Visualization with Matplotlib ---
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 8), sharex=True)

# Plot Max Wind Speed in Beaufort Scale
axes[0].plot(df.index, df['beaufort_wind_speed'], marker='o', linestyle='-', color='b')
axes[0].set_title(f'Beaufort Scale Max Wind Speed (Last {PAST_DAYS} Days)')
axes[0].set_ylabel('Beaufort Scale')
axes[0].grid(True, which='both', linestyle='--', linewidth=0.5)
axes[0].set_ylim(-0.5, 12.5) # Set y-axis limits to clearly show Beaufort values 0-12
axes[0].set_yticks(np.arange(0, 13, 1)) # Display a tick for each Beaufort value

# Plot Max Wind Gusts in Beaufort Scale
axes[1].plot(df.index, df['beaufort_wind_gust'], marker='o', linestyle='--', color='r')
axes[1].set_title(f'Beaufort Scale Max Wind Gusts (Last {PAST_DAYS} Days)')
axes[1].set_ylabel('Beaufort Scale')
axes[1].set_xlabel('Date')
axes[1].grid(True, which='both', linestyle='--', linewidth=0.5)
axes[1].set_ylim(-0.5, 12.5)
axes[1].set_yticks(np.arange(0, 13, 1))

# Format x-axis for clear dates (shared by both plots)
axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
axes[1].xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.suptitle('Daily Wind Conditions (Beaufort Scale) in Banda Aceh', y=1.02, fontsize=16)
plt.show()

print("\n--- DataFrame with Beaufort Scale values ---")
print(df[['beaufort_wind_speed', 'beaufort_wind_gust']])
