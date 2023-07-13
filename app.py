import streamlit as st



# sidebar elements
st.sidebar.write("Settings")

# main page
st.title("Data Drift Detection")
st.markdown("The following app is to be used **ONLY** for internal purpose")


tab0, tab1, tab2 = st.tabs(["Explanation", "Input data", "Output data"])