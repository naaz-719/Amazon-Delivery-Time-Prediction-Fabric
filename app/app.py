import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Amazon Delivery Time Prediction",
    page_icon="🚚",
    layout="wide"
)

# =========================================================
# LOAD MODEL
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(
    BASE_DIR,
    "..",
    "models",
    "final_streamlit_model.pkl"
)

model = joblib.load(model_path)

# =========================================================
# TITLE
# =========================================================

st.title("🚚 Amazon Delivery Time Prediction")

st.markdown("""
Predict estimated delivery times using Machine Learning.

### Technologies Used
- Microsoft Fabric
- Medallion Architecture
- MLflow
- Scikit-learn
- Streamlit
""")

# =========================================================
# SIDEBAR INPUTS
# =========================================================

st.sidebar.header("📦 Delivery Details")

agent_age = st.sidebar.slider(
    "Agent Age",
    18,
    60,
    30
)

agent_rating = st.sidebar.slider(
    "Agent Rating",
    1.0,
    5.0,
    4.0
)

weather = st.sidebar.selectbox(
    "Weather Condition",
    [
        "Sunny",
        "Cloudy",
        "Fog",
        "Stormy",
        "Windy"
    ]
)

traffic = st.sidebar.selectbox(
    "Traffic Condition",
    [
        "Low",
        "Medium",
        "High",
        "Jam"
    ]
)

vehicle = st.sidebar.selectbox(
    "Vehicle Type",
    [
        "Bike",
        "Scooter",
        "Car"
    ]
)

area = st.sidebar.selectbox(
    "Area Type",
    [
        "Urban",
        "Metropolitan"
    ]
)

category = st.sidebar.selectbox(
    "Product Category",
    [
        "Electronics",
        "Clothing",
        "Food",
        "Cosmetics",
        "Sports",
        "Books",
        "Home"
    ]
)

distance_km = st.sidebar.slider(
    "Distance (km)",
    1.0,
    30.0,
    5.0
)

order_hour = st.sidebar.slider(
    "Order Hour",
    0,
    23,
    12
)

pickup_hour = st.sidebar.slider(
    "Pickup Hour",
    min_value=order_hour,
    max_value=23,
    value=max(order_hour, 13)
)



is_weekend = st.sidebar.selectbox(
    "Is Weekend?",
    [0, 1]
)

if is_weekend == 1:

    day_of_week = st.sidebar.selectbox(
        "Day of Week",
        [
            "Saturday",
            "Sunday"
        ]
    )

else:

    day_of_week = st.sidebar.selectbox(
        "Day of Week",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]
    )

is_rush_hour = st.sidebar.selectbox(
    "Rush Hour",
    [0, 1]
)

# =========================================================
# INPUT DATAFRAME
# =========================================================

input_data = pd.DataFrame({

    "Agent_Age": [agent_age],

    "Agent_Rating": [agent_rating],

    "Weather": [weather],

    "Traffic": [traffic],

    "Vehicle": [vehicle],

    "Area": [area],

    "Category": [category],

    "Distance_km": [distance_km],

    "order_hour": [order_hour],

    "pickup_hour": [pickup_hour],

    "day_of_week": [day_of_week],

    "is_weekend": [is_weekend],

    "is_rush_hour": [is_rush_hour]
})

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs([
    "Prediction",
    "Business Insights",
    "Project Overview"
])

# =========================================================
# TAB 1 — PREDICTION
# =========================================================

with tab1:

    st.subheader("📍 Delivery Prediction")

    st.write("### Input Summary")

    st.dataframe(input_data)

    if st.button("Predict Delivery Time"):

        prediction = model.predict(input_data)[0]

        st.success(
            f"Estimated Delivery Time: {prediction:.2f} minutes"
        )

        # Operational Insights

        if traffic in ["High", "Jam"]:
            st.warning(
                "Heavy traffic conditions may increase delivery delays."
            )

        if distance_km > 15:
            st.info(
                "Long-distance deliveries usually require additional time."
            )

        if is_rush_hour == 1:
            st.warning(
                "Rush hour traffic detected."
            )

# =========================================================
# TAB 2 — BUSINESS INSIGHTS
# =========================================================

with tab2:

    st.subheader("📊 Operational Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Delivery Time",
        "42 mins"
    )

    col2.metric(
        "Best Traffic Condition",
        "Low"
    )

    col3.metric(
        "Most Efficient Vehicle",
        "Bike"
    )

    # Traffic Chart

    traffic_data = pd.DataFrame({

        "Traffic": [
            "Low",
            "Medium",
            "High",
            "Jam"
        ],

        "Average_Time": [
            25,
            38,
            52,
            68
        ]
    })

    fig1 = px.bar(

        traffic_data,

        x="Traffic",

        y="Average_Time",

        title="Traffic Impact on Delivery Time"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # Distance Chart

    distance_data = pd.DataFrame({

        "Distance_km": [
            2,
            5,
            8,
            12,
            18,
            25
        ],

        "Delivery_Time": [
            18,
            25,
            32,
            45,
            60,
            78
        ]
    })

    fig2 = px.line(

        distance_data,

        x="Distance_km",

        y="Delivery_Time",

        markers=True,

        title="Distance vs Delivery Time"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =========================================================
# TAB 3 — PROJECT OVERVIEW
# =========================================================

with tab3:

    st.subheader("📘 Project Architecture")

    st.markdown("""

### 🔹 Architecture

Bronze Layer → Raw Data  
Silver Layer → Cleaned Data  
Gold Layer → Feature Engineered Data  
ML Pipeline → Model Training & Evaluation  
MLflow → Experiment Tracking  
Streamlit → Deployment Interface  

---

### 🔹 Machine Learning Models

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor
- Hyperparameter Tuning using RandomizedSearchCV

---

### 🔹 Technologies Used

- Microsoft Fabric
- PySpark
- Pandas
- Scikit-learn
- MLflow
- Streamlit
- Plotly
- GitHub

---

### 🔹 Key Features Engineered

- Distance Calculation
- Rush Hour Detection
- Weekend Identification
- Day-of-Week Analysis
- Time-Based Features
- Traffic & Weather Encoding

---

### 🔹 Business Objective

Predict delivery times accurately to:
- optimize logistics operations
- reduce delays
- improve customer satisfaction
- improve delivery planning

---

### 🔹 Future Enhancements

- Live GPS integration
- Google Maps API integration
- Real-time traffic APIs
- Route optimization engine
- Real-time ETA tracking
""")



# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Built using Microsoft Fabric, MLflow, and Streamlit"
)