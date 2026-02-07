import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:shivanika@localhost:3306/earthquakes_db"
)

def get_data(query, params=None):
    if params:
        return pd.read_sql(query, engine, params=params)
    return pd.read_sql(query, engine)

# -------------------- STREAMLIT CONFIG --------------------
st.set_page_config(page_title="Earthquake Data Analysis", layout="wide")

# Sidebar Navigation
st.sidebar.title("🌍 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Project Introduction", "Earthquake Visualization", "SQL Analysis", "Creator Info"]
)

# -------------------- PAGE 1: INTRODUCTION --------------------
if page == "Project Introduction":
    st.title("🌏 Earthquake Data Analysis")
    st.subheader("📊 Global Seismic Activity Dashboard")

    st.write("""
    This project analyzes global earthquake data collected from the USGS API.
    The data is stored in a MySQL database and analyzed using SQLAlchemy and Streamlit.

    **Features**
    - Interactive filters (country, date, magnitude)
    - Time-based and depth-based analysis
    - SQL-driven insights
    - Visual analytics dashboard

    **Database:** earthquakes_db  
    **Table:** earthquakes
    """)

# -------------------- PAGE 2: VISUALIZATION --------------------
elif page == "Earthquake Visualization":
    st.title("📈 Earthquake Visualizations")

    # -----------------------------
    # Load regions (extracted from place)
    # -----------------------------
    regions = get_data(
        """
        SELECT DISTINCT
               TRIM(SUBSTRING_INDEX(place, ',', -1)) AS region
        FROM earthquakes
        WHERE place IS NOT NULL
        """
    )["region"].tolist()

    selected_region = st.selectbox("🌍 Select Region / Country", regions)

    # -----------------------------
    # Filters
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        mag_range = st.slider(
            "📊 Magnitude Range",
            4.0, 9.5, (4.0, 7.5)
        )

    with col2:
        date_range = st.date_input(
            "📅 Date Range",
            []
        )

    # -----------------------------
    # Query
    # -----------------------------
    query = """
        SELECT time, mag, depth_km, place, latitude, longitude
        FROM earthquakes
        WHERE place LIKE %s
        AND mag BETWEEN %s AND %s
        ORDER BY time
    """

    df = get_data(
        query,
        params=(f"%{selected_region}%", mag_range[0], mag_range[1])
    )

    df["time"] = pd.to_datetime(df["time"])

    # Date filter (optional)
    if len(date_range) == 2:
        df = df[
            (df["time"].dt.date >= date_range[0]) &
            (df["time"].dt.date <= date_range[1])
        ]

    # -----------------------------
    # Display Results
    # -----------------------------
    if not df.empty:

        # -------- Summary Metrics --------
        st.subheader("📊 Summary")
        m1, m2, m3 = st.columns(3)

        m1.metric("Total Earthquakes", len(df))
        m2.metric("Max Magnitude", round(df["mag"].max(), 2))
        m3.metric("Avg Depth (km)", round(df["depth_km"].mean(), 2))

        # -------- Data Table --------
        st.subheader("📄 Earthquake Records")
        st.dataframe(
            df[["time", "mag", "depth_km", "place"]],
            use_container_width=True
        )

        # -------- Magnitude Trend --------
        st.subheader("🔥 Magnitude Trend Over Time")
        plt.figure(figsize=(10, 4))
        plt.plot(df["time"], df["mag"], marker="o")
        plt.xlabel("Time")
        plt.ylabel("Magnitude")
        plt.title("Earthquake Magnitude Over Time")
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # -------- Depth Distribution --------
        st.subheader("🌊 Depth Distribution")
        plt.figure(figsize=(6, 4))
        plt.hist(df["depth_km"], bins=20)
        plt.xlabel("Depth (km)")
        plt.ylabel("Frequency")
        plt.title("Earthquake Depth Distribution")
        st.pyplot(plt)

        # -------- Map Visualization --------
        st.subheader("🗺️ Earthquake Map")
        map_df = df.rename(columns={"latitude": "lat", "longitude": "lon"})
        st.map(map_df[["lat", "lon"]])

    else:
        st.warning("⚠️ No earthquake data for selected filters.")

        # -------------------- PAGE 3: SQL ANALYSIS --------------------
elif page == "SQL Analysis":

    st.title("📋 Earthquake SQL Insights")

    queries = {

        # ---------------- Magnitude & Depth ----------------

        "1. Top 10 Strongest Earthquakes":
        """
        SELECT place, mag, depth_km, time
        FROM earthquakes
        ORDER BY mag DESC
        LIMIT 10
        """,

        "2. Top 10 Deepest Earthquakes":
        """
        SELECT place, depth_km, mag
        FROM earthquakes
        ORDER BY depth_km DESC
        LIMIT 10
        """,

        "3. Shallow (<50km) & Mag > 7.5":
        """
        SELECT place, mag, depth_km
        FROM earthquakes
        WHERE depth_km < 50 AND mag > 7.5
        """,

        

        "5. Avg Magnitude by magType":
        """
        SELECT magType, AVG(mag) AS avg_mag
        FROM earthquakes
        GROUP BY magType
        """,

        # ---------------- Time Analysis ----------------

        "6. Year with Most Earthquakes":
        """
        SELECT YEAR(time) AS year, COUNT(*) AS total
        FROM earthquakes
        GROUP BY year
        ORDER BY total DESC
        LIMIT 1
        """,

        "7. Month with Highest Earthquakes":
        """
        SELECT MONTH(time) AS month, COUNT(*) AS total
        FROM earthquakes
        GROUP BY month
        ORDER BY total DESC
        LIMIT 1
        """,

        "8. Most Active Day of Week":
        """
        SELECT DAYNAME(time) AS day, COUNT(*) AS total
        FROM earthquakes
        GROUP BY day
        ORDER BY total DESC
        """,

        "9. Earthquakes per Hour":
        """
        SELECT HOUR(time) AS hour, COUNT(*) AS total
        FROM earthquakes
        GROUP BY hour
        ORDER BY hour
        """,

        "10. Most Active Reporting Network":
        """
        SELECT net, COUNT(*) AS total
        FROM earthquakes
        GROUP BY net
        ORDER BY total DESC
        LIMIT 1
        """,

        # ---------------- Impact & Type ----------------

        "11. Top 5 Places with Highest Significance":
        """
        SELECT place, SUM(sig) AS total_significance
        FROM earthquakes
        GROUP BY place
        ORDER BY total_significance DESC
        LIMIT 5
        """,

        

        "13. Earthquakes with High Magnitude & High Depth":
        """
        SELECT place, mag, depth_km
        FROM earthquakes
        WHERE mag > 6 AND depth_km > 300
        """,

        "14. Reviewed vs Automatic Events":
        """
        SELECT status, COUNT(*) AS total
        FROM earthquakes
        GROUP BY status
        """,

        "15. Count by Earthquake Type":
        """
        SELECT type, COUNT(*) AS total
        FROM earthquakes
        GROUP BY type
        """,

        "16. Count by Data Type":
        """
        SELECT types, COUNT(*) AS total
        FROM earthquakes
        GROUP BY types
        """,

        "17. Average RMS Error":
        """
        SELECT AVG(rms) AS avg_rms_error
        FROM earthquakes
        """,

        "18. High Station Coverage (nst > 50)":
        """
        SELECT COUNT(*) AS high_station_events
        FROM earthquakes
        WHERE nst > 50
        """,

        # ---------------- Tsunami & Alerts ----------------

        "19. Tsunamis per Year":
        """
        SELECT YEAR(time) AS year, SUM(tsunami) AS total
        FROM earthquakes
        GROUP BY year
        ORDER BY year
        """,

        "20. Total Tsunami Events":
        """
        SELECT COUNT(*) AS total_tsunamis
        FROM earthquakes
        WHERE tsunami = 1
        """,

        # ---------------- Advanced Analysis ----------------

        "21. Top 5 Countries (Avg Mag - 10 Years)":
        """
        SELECT place, AVG(mag) AS avg_mag
        FROM earthquakes
        WHERE YEAR(time) >= YEAR(CURDATE()) - 10
        GROUP BY place
        ORDER BY avg_mag DESC
        LIMIT 5;
        """,


        "22. Countries with Shallow & Deep in Same Month":
        """
        SELECT 
        SUBSTRING_INDEX(place, ',', -1) AS country
        FROM earthquakes
        GROUP BY country, YEAR(time), MONTH(time)
        HAVING
        SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) > 0
        AND
        SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END) > 0;
        """,

        "23. Year-over-Year Earthquake Growth (%)":
        """
        SELECT year,
               total,
               ROUND(
                   (total - LAG(total) OVER (ORDER BY year)) /
                   LAG(total) OVER (ORDER BY year) * 100, 2
               ) AS yoy_growth_percent
        FROM (
            SELECT YEAR(time) AS year, COUNT(*) AS total
            FROM earthquakes
            GROUP BY year
        ) t
        """,

        "24. Top 3 Seismically Active Regions":
        """
       SELECT place,
       COUNT(*) AS frequency,
       AVG(mag) AS avg_magnitude,
       COUNT(*) * AVG(mag) AS activity_score
       FROM earthquakes
       GROUP BY place
       ORDER BY activity_score DESC
       LIMIT 3;
       """,

        "25. Avg Depth Near Equator (±5° Latitude)":
        """
        SELECT 
        SUBSTRING_INDEX(place, ',', -1) AS country,
        AVG(depth_km) AS avg_depth
        FROM earthquakes
        WHERE latitude BETWEEN -5 AND 5
        GROUP BY country
        ORDER BY avg_depth DESC
        """,

        

        "26. Highest Shallow-to-Deep Ratio":
        """
        SELECT 
        SUBSTRING_INDEX(place, ',', -1) AS country,
        SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) /
        NULLIF(SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END), 0)
        AS shallow_to_deep_ratio
        FROM earthquakes
        GROUP BY country
        ORDER BY shallow_to_deep_ratio DESC;
        """,


        "27. Avg Magnitude Difference (Tsunami vs Non-Tsunami)":
        """
        SELECT ROUND(
            AVG(CASE WHEN tsunami = 1 THEN mag END) -
            AVG(CASE WHEN tsunami = 0 THEN mag END),
        2) AS magnitude_difference
        FROM earthquakes
        """,

        "28. Lowest Data Reliability (High Error Score)":
        """
        SELECT id, place,
               (IFNULL(gap,0) + IFNULL(rms,0)) AS error_score
        FROM earthquakes
        ORDER BY error_score DESC
        LIMIT 10
        """,

        "29. Total Earthquakes per Country":
        """
        SELECT 
        SUBSTRING_INDEX(place, ',', -1) AS country,
        COUNT(*) AS total_earthquakes
        FROM earthquakes
        GROUP BY country
        ORDER BY total_earthquakes DESC
        """,


        
    "30.Top 10 Deep Earthquakes by Place":
    """
    SELECT place, COUNT(*) AS total
    FROM earthquakes
    WHERE depth_km > 300
    GROUP BY place
    ORDER BY total DESC
    LIMIT 10
    """
    }
    selected_query = st.selectbox("Choose Analysis", list(queries.keys()))
    result_df = get_data(queries[selected_query])
    st.dataframe(result_df, use_container_width=True)


# ---------------- CREATOR INFO ----------------
elif page == "Creator Info":
    st.title("👩‍💻 Project Creator")
    st.write("""
    **Name:** Palanikumari  
    **Skills:** Python, SQL, Data Analysis, Streamlit, Pandas  
    **Project:** Earthquake Analytics Dashboard
    """)
    st.success("🚀 Built using USGS data, SQLAlchemy & Streamlit")


       