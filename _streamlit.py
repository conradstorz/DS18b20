#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import requests
from pprint import pprint
import json
import pandas as pd

def send_tweet(tweet):
    """Uses ThingSpeak ThingTweet to send tweets.

    Args:
        tweet (Str): A valid tweet string
    """
    API_KEY = '943KI9M4I2TU316Q'
    TWEET = 'HeyWorld'
    update_url_target = f'https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key={API_KEY}&status={TWEET}'
    print(update_url_target)
    with urllib.request.urlopen(update_url_target) as response:
        html = response.read()
    return

def get_json_from_ThingSpeak(url):
    """Returns string of JSON from ThingSpeak website.

    Args:
        url (str): A valid URL request for JSON data.
    """
    response = requests.get(url)
    print(f'The website URL returned an item typed: {type(response)}')
    r = response.content.decode('utf-8')
    print(f'with a content of type:{type(r)}')
    return r


def display_details_of_json_str(s):
    """Display and Return a dict.

    Args:
        s (str): JSON formatted string

    Returns:
        dict: JSON string converted to dict.
    """
    str_data = json.loads(s)
    print(f'JSON string converted to type:{type(str_data)}')
    print(f'Converted JSON contains {len(str_data)} items.')
    print()
    for k, v in str_data.items():
        print(f'The KEY:"{k}" contains {len(v)} items.')
        print(f'and is of type {type(v)}')
        #pprint(v)
        print()
    return str_data


url_str = 'https://api.thingspeak.com/channels/1216774/feeds.json'

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


"""
import streamlit as st
import time
import numpy as np

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
"""


"""
import streamlit as st
import pandas as pd
import altair as alt

@st.cache
def get_UN_data():
    AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")

try:
    df = get_UN_data()
except urllib.error.URLError as e:
    st.error(
        "**This demo requires internet access.** Connection error: %s" % e.reason
    )
    return

countries = st.multiselect(
    "Choose countries", list(df.index), ["China", "United States of America"]
)
if not countries:
    st.error("Please select at least one country.")
    return

data = df.loc[countries]
data /= 1000000.0
st.write("### Gross Agricultural Production ($B)", data.sort_index())

data = data.T.reset_index()
data = pd.melt(data, id_vars=["index"]).rename(
    columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
)
chart = (
    alt.Chart(data)
    .mark_area(opacity=0.3)
    .encode(
        x="year:T",
        y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
        color="Region:N",
    )
)
st.altair_chart(chart, use_container_width=True)
"""
