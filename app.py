import streamlit as st
import pandas as pd 

from src.data_handler import DataHandler

# sidebar elements
st.sidebar.write("Settings")
p_threshold = st.sidebar.slider("Select a p-value threshold", min_value=0.0,
                                max_value=1.0, step=0.05, value=0.05)
cat_algorithm = st.sidebar.selectbox(label="Select detection algorithm for categorical columns",
                                     options=['chi-square test'])
num_algorithm = st.sidebar.selectbox(label="Select detection algorithm for numerical columns",
                                     options=['kolmogorov-smirnov test'])

# main page
st.title("Data Drift Detection")
st.markdown("The following app is can be used to detect covariate data drift")


tab0, tab1, tab2 = st.tabs(["Guidelines", "Data", "Analysis"])

# Tab 0 - Guidelines

# Tab 1 - Data 

tab1.markdown("###### Upload dataframes")
target_file = tab1.file_uploader("Choose a target dataframe")
source_file = tab1.file_uploader("Choose a source dataframe")

if target_file is not None and source_file is not None:
    target_df = pd.read_csv(target_file)
    source_df = pd.read_csv(source_file)

    # The data handler object 
    dh = DataHandler(target=target_df,
                     source=source_df)

    tab1.markdown("###### Target dataframe")
    tab1.dataframe(dh.target)

    tab1.markdown("###### Source dataframe")
    tab1.dataframe(dh.source)

    dh.check_columns()
    dh.coerce_quality()

    tab1.markdown("###### Column types")
    tab1.dataframe(dh.type_df)

    # tab1.markdown("###### Override column types")
    # tab1col1, tab1col2 = tab1.columns(2)
    # with tab1col1:
    #     column = st.selectbox(label="Select a column", 
    #                            options=list(dh.source.columns))

    # with tab1col2:
    #     type = st.selectbox(label="Select a type",
    #                          options=['id', 'categorical', 'numerical', 'date'])

    # if tab1.button(label="Add constraint"):
    #     old_type = dh.type_df[dh.type_df['column_names']==column]['column_types'].values[0]
    #     dh.type_df.loc[(dh.type_df['column_names']==column) & (dh.type_df['column_types']==old_type)] = [[column,type]]     

    # tab1.markdown("###### New column types")
    # tab1.dataframe(dh.type_df)


# Tab 2 - Analysis

if target_file is not None and source_file is not None:
    tab2.markdown("###### Analysis result")
    dh.analye(p_threshold)
    tab2.dataframe(dh.result_df)

    tab2.markdown("###### Visualisation")
    vis_col = tab2.selectbox(label="select a column to visualise", 
                             options= dh.type_df['column_names'].unique())
    
    tab2.plotly_chart(dh.visualise(column_name=vis_col), use_container_width=True)