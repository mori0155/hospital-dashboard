import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Hospital Capacity Dashboard", layout="wide")

## 1. Create Dummy Data
def load_data():
    data = {
        'Ward': ['ICU', 'General', 'Maternity', 'ICU', 'General', 'Maternity'],
        'Status': ['Occupied', 'Occupied', 'Occupied', 'Available', 'Available', 'Available'],
        'Beds': [12, 45, 20, 3, 15, 10]
    }
    return pd.DataFrame(data)

df = load_data()

## 2. Header and Sidebar
st.title("🏥 Hospital Bed Capacity Dashboard")
st.markdown("Monitor real-time bed availability across different departments.")

## 3. Add a Slider to Filter Data
# We will use a slider to filter by a minimum number of available beds
st.sidebar.header("Filters")
min_beds = st.sidebar.slider("Filter by Minimum Beds", 0, 50, 0)

# Apply filter
filtered_df = df[df['Beds'] >= min_beds]

## 4. Layout: Metrics and Bar Chart
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Key Metrics")
    total_occupied = df[df['Status'] == 'Occupied']['Beds'].sum()
    total_available = df[df['Status'] == 'Available']['Beds'].sum()
    
    st.metric("Total Occupied", total_occupied)
    st.metric("Total Available", total_available, delta_color="normal")

with col2:
    st.subheader("Occupancy by Ward")
    # Create the Bar Chart
    fig = px.bar(
        filtered_df, 
        x="Ward", 
        y="Beds", 
        color="Status",
        barmode="group",
        color_discrete_map={'Occupied': '#EF553B', 'Available': '#00CC96'},
        text_auto=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

## 5. Data Table
st.subheader("Detailed Ward Data")
st.dataframe(filtered_df, use_container_width=True)
