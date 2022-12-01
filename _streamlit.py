#!/usr/bin/env python
# -*- coding: utf-8 -*-


import streamlit as st

from Temperature_Mon._thingspeak import url_list
from Temperature_Mon._thingspeak import pandas_dataframe


st.title('Hello World')

DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    df = pandas_dataframe(url_list)     
    return df


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done! (using st.cache)')
st.subheader('Raw data')
st.write(data)
st.line_chart(data)

def Main():

    print(data)

    def time_period():
        """[summary]
        """

    def show_plot():
        """
        """

