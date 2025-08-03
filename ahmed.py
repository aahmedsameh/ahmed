#import libraries
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Read data
df = pd.read_csv("sleep.csv")
print(df.head())

# Cleaning
df['Sleep Disorder'] = df['Sleep Disorder'].replace(np.nan, 'Normal')

# Sidebar
st.sidebar.header("Sleep dashboard")
st.sidebar.image('15-ronaldo-facts-fans-should-know-1714300205.jpg')
# st.sidebar.write('The purpose of the dashboard is to show the reasons for sleep disorder')

# Sidebar filter
cat_filter = st.sidebar.selectbox('Filters', ['Gender', 'Occupation', 'BMI Category', None, 'Sleep Disorder'])

# KPIs
a1, a2, a3, a4 = st.columns(4)
a1.metric("Avg age", round(df['Age'].mean(), 2))
a2.metric("Count of ID", df['Person ID'].count())
a3.metric("Max daily steps", df['Daily Steps'].max())
a4.metric("Avg sleep duration", round(df['Sleep Duration'].mean(), 2))

st.subheader('Sleep quality vs stress level')

# Handle None in cat_filter before plotting
if cat_filter is not None and cat_filter in df.columns:
    fig = px.scatter(data_frame=df, x='Stress Level', y='Quality of Sleep', color=cat_filter, size='Quality of Sleep')
else:
    fig = px.scatter(data_frame=df, x='Stress Level', y='Quality of Sleep', size='Quality of Sleep')

st.plotly_chart(fig, use_container_width=True)

# Bottom charts
c1, c2 = st.columns([4, 3])

with c1:
    st.text("Occupation vs Avg Sleep Duration (Sorted)")

    # Calculate average sleep duration by occupation and sort descending
    avg_sleep_by_occ = (
        df.groupby('Occupation')['Sleep Duration']
        .mean()
        .sort_values(ascending=False))
