# Open-Meteo Wind Data Visualization
This repository contains a Python project designed to visualize historical weather data for a specific location. By leveraging the Open-Meteo API, the script fetches daily weather metrics - including temperature and wind conditions - and presents them in clear, insightful graphs. This tool is perfect for anyone who wants to quickly analyze recent weather patterns without complex setup.

#### Features
- API Integration: Automatically retrieves historical daily weather data, such as temperature, wind speed, and wind gusts, for the last 14 days from the free Open-Meteo API.
- Data Processing: Utilizes the pandas library to structure the raw API data into a clean, easy-to-use DataFrame for analysis.
- Comprehensive Visualization: Generates two distinct and professional-looking graphs using matplotlib:
- Temperature Graph: A line graph showing the daily minimum and maximum temperatures.
- Wind Graph: A two-row plot displaying separate line graphs for daily maximum wind speed and wind gusts, making it simple to compare their trends.
- Customizable: The script is easily configurable. Users can change the location's latitude and longitude, as well as the number of past days to be analyzed, directly within the code.
