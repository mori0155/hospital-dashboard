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
# We will use a slider to filter by minimum % of available beds
st.sidebar.header("Filters")
min_availability_pct = st.sidebar.slider("Filter by Minimum % Available Beds", 0, 100, 0)

# Calculate availability percentage by ward
ward_availability = df.groupby('Ward').apply(
    lambda x: (x[x['Status'] == 'Available']['Beds'].sum() / x['Beds'].sum() * 100)
).reset_index()
ward_availability.columns = ['Ward', 'availability_pct']

# Get wards that meet the filter criteria
filtered_wards = ward_availability[ward_availability['availability_pct'] >= min_availability_pct]['Ward'].values

# Apply filter
filtered_df = df[df['Ward'].isin(filtered_wards)]

## 4. Layout: Metrics and Bar Chart
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Key Metrics")
    total_occupied = df[df['Status'] == 'Occupied']['Beds'].sum()
    total_available = df[df['Status'] == 'Available']['Beds'].sum()
    total_beds = df['Beds'].sum()
    overall_occupancy_pct = (total_occupied / total_beds * 100) if total_beds > 0 else 0
    
    st.metric("Total Occupied", total_occupied)
    st.metric("Total Available", total_available, delta_color="normal")
    st.metric("Overall Occupancy %", f"{overall_occupancy_pct:.1f}%")

with col2:
    st.subheader("Occupancy by Ward")
    # Create the Bar Chart
    fig = px.bar(
        filtered_df, 
        x="Ward", 
        y="Beds", 
        color="Status",
        barmode="stack",
        color_discrete_map={'Occupied': '#EF553B', 'Available': '#00CC96'},
        text_auto=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

## 5. Ward Occupancy Percentages
st.subheader("Ward Occupancy Percentages")
ward_summary = df.pivot_table(values='Beds', index='Ward', columns='Status', aggfunc='sum', fill_value=0).reset_index()
ward_summary['total_beds'] = ward_summary['Occupied'] + ward_summary['Available']
ward_summary['occupancy_pct'] = (ward_summary['Occupied'] / ward_summary['total_beds'] * 100).round(1)

st.dataframe(ward_summary[['Ward', 'total_beds', 'Occupied', 'Available', 'occupancy_pct']], use_container_width=True)

## 6. Data Table
st.subheader("Detailed Ward Data")
st.dataframe(filtered_df, use_container_width=True)
