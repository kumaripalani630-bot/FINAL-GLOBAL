# FINAL-GLOBAL
Earthquakes insights
Global Seismic Trends: Data-Driven Earthquake Insights.
Project Title:
Gobal Seismic Trends – Earthquake Data Analysis and Visualization

Objective:
The main objective of this project is to analyze global earthquake data to
identify seismic patterns, magnitude and depth trends, and high-risk regions.
The project also aims to present these insights through an interactive
Streamlit dashboard for easy exploration and understanding.

Dataset Source:
The dataset is collected from the United States Geological Survey (USGS)
Earthquake API.
It contains real-time and historical earthquake records including:
Magnitude
Depth
Latitude & Longitude
Location
Time of occurrence

Tools & Technologies:
Python – Data processing and analysis
Pandas & NumPy – Data cleaning and transformation
Matplotlib – Data visualization
MySQL – Database storage
SQLAlchemy – Database connectivity
Streamlit – Interactive dashboard development
Git & GitHub – Version control and project hosting

Project Workflow:
Collect earthquake data from the USGS API
Clean and preprocess the data
Handle missing values
Convert timestamps
Feature engineering (year, month, depth category)
Store the cleaned data in a MySQL database
Perform SQL queries to extract insights

Build an interactive Streamlit dashboard for visualization:
Features
Global earthquake trend analysis
Magnitude-wise and depth-wise insights
Identification of deep-focus earthquakes
Year-wise and region-wise filtering
Interactive charts and visualizations
User-friendly Streamlit dashboard

How to Run (Important 🔥)
Step 1: Install required libraries
pip install pandas numpy matplotlib streamlit sqlalchemy pymysql

Step 2: Create MySQL database
CREATE DATABASE earthquakes_db;

Step 3: Run the Streamlit application
streamlit run app.py

Dashboard Preview (Optional):
The Streamlit dashboard provides interactive visualizations of global
earthquake activity. Users can filter data based on year, magnitude,
and depth to gain meaningful insights into seismic trends.
