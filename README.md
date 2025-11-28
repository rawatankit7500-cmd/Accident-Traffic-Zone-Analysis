# Accident & Traffic Zone Analysis

A Flask-based Accident and Traffic Zone Analysis Web App that shows:
- Heatmap of accident hotspots
- Dynamic charts (pie & bar)
- Interactive map using Folium
- User authentication (Signup/Login)
- CSV-based accident dataset analysis

## Features
### 1. User Authentication
Signup and Login system using SQLite database.

### 2. Accident Heatmap
Displays accident density using Folium HeatMap.

### 3. Charts & Visualization
- Pie chart for Severity Distribution
- Bar chart for Vehicle Type Comparison

### 4. Area-Wise Search
Enter an area like:
- Prem Nagar
- ISBT
- Rajpur Road
- Clock Tower  
and view complete analysis.

## Project Structure
- app.py  
- accidents_in_dehradun.csv  
- templates (HTML files)  
- static (charts, css, map files)  

## How it works
1. User signs up or logs in  
2. User enters any area  
3. The app loads data from CSV  
4. It generates:
   - Accident map  
   - Severity pie chart  
   - Vehicle type bar chart  
5. Results appear on a beautiful dashboard  

## Tech Stack
- Python  
- Flask  
- Folium  
- Chart.js  
- HTML/CSS  
- SQLite
