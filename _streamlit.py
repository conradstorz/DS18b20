#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from pprint import pprint
import json
import datetime
import streamlit as st
import pandas as pd
import numpy as np

st.title('Hello World')
span = '?days=1'
url_str = f'https://api.thingspeak.com/channels/1216774/feeds.json{span}'


DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    return


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done! (using st.cache)')
data = data.set_index('created_at')
st.subheader('Raw data')
st.write(data)

#hist_values = np.histogram(data['created_at'])
st.line_chart(data)

def Main():
    json_str = get_json_from_ThingSpeak(url_str)

    dict_data = display_details_of_json_str(json_str)

    feeds_dataframe = pd.DataFrame(dict_data["feeds"])

    print(feeds_dataframe)

    def time_period():
        """[summary]
        """

    def show_plot():
        """
        """

