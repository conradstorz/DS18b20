#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
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
    r = requests.get(url_str)
    j = r.json()
    df = pd.DataFrame(j['feeds'])
    df = df.drop(['entry_id'], axis=1)
    df["created_at"] = pd.to_datetime(df['created_at'], format="%Y-%m-%dT%H:%M:%SZ")
    df.set_index('created_at')
    #df = df.apply(pd.to_numeric) # convert all columns of DataFrame
    # line above changes datetime obj to int64
    # convert just columns "field1", 'field2', 'field3', 'field4' and "field5"
    field_list = ['field1', 'field2', 'field3', 'field4', 'field5']
    df[field_list] = df[field_list].apply(pd.to_numeric)    
    return df

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

