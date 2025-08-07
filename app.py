import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# List of Excel files to append
excel_files = ['2009.xlsx', '2010.xlsx', '2011.xlsx', '2012.xlsx']

# Read and append all files into one DataFrame
df_list = [pd.read_excel(file) for file in excel_files]
combined_df = pd.concat(df_list, ignore_index=True)

# Clean the DataFrame
combined_df.columns = [col.strip().lower().replace(' ', '_') for col in combined_df.columns]
combined_df = combined_df.dropna(axis=1, how='all')
combined_df = combined_df.drop_duplicates()
combined_df = combined_df.dropna()
combined_df = combined_df.convert_dtypes()

sorted_df = combined_df.sort_values(by=combined_df.columns.tolist(), ascending=True)

# Streamlit app
st.set_page_config(page_title='Excel Data Insights', page_icon='📊', layout='wide')
st.title('📊 Excel Data Insights and Visuals')
st.caption('Explore, filter, and visualize your cleaned Excel data interactively!')

sidebar = st.sidebar
sidebar.header('Filter Data')
filter_col = sidebar.multiselect('Select columns to display:', sorted_df.columns.tolist(), default=sorted_df.columns.tolist())

cat_cols = sorted_df.select_dtypes(include='object').columns.tolist()
cat_filters = {}
for col in cat_cols:
    unique_vals = sorted_df[col].unique().tolist()
    selected_vals = sidebar.multiselect(f'Filter {col}:', unique_vals, default=unique_vals)
    cat_filters[col] = selected_vals

# Apply filters
filtered_df = sorted_df[filter_col]
for col, vals in cat_filters.items():
    filtered_df = filtered_df[filtered_df[col].isin(vals)]

st.subheader('🔎 Filtered Data')
st.dataframe(filtered_df, use_container_width=True)

st.markdown('---')
st.subheader('🧮 DataFrame Info')
st.text(f"Rows: {filtered_df.shape[0]}, Columns: {filtered_df.shape[1]}")
st.write(filtered_df.describe())

st.markdown('---')
st.subheader('🌈 Key Insights')
st.success(f"The dataset contains {filtered_df.shape[0]} rows after filtering.")
st.info(f"Columns available: {', '.join(filter_col)}")
if cat_cols:
    for col in cat_cols:
        st.caption(f"Most common value in '{col}': {filtered_df[col].mode()[0] if not filtered_df.empty else 'N/A'}")

st.markdown('---')
st.subheader('📈 Visualizations')
numeric_cols = filtered_df.select_dtypes(include='number').columns.tolist()
if numeric_cols:
    col = st.selectbox('Select a numeric column for chart:', numeric_cols)
    st.markdown(f"**Histogram of {col}**")
    st.bar_chart(filtered_df[col], use_container_width=True)
    st.markdow
