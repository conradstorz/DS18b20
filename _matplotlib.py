#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 2.0
"""Create a plot of datapoints from ThingSpeak.
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt

channel1 = '1216774'
channel2 = '1239835'
channels = [channel1, channel2]

url_str_base = 'https://api.thingspeak.com/channels/'
url_str_tail = '/feeds.json?days=2'

url1 = f'{url_str_base}{channel1}{url_str_tail}'
url2 = f'{url_str_base}{channel2}{url_str_tail}'


def load_json_data_into_dict(url):
    """Return a dict from a JSON source
    """
    r = requests.get(url)
    j = r.json()
    return j


def split_dicts_from_raw_data(json_dict):
    """Split channels and feeds dicts.
    """
    jcd = json_dict['channel'] # equals a dict
    print(f'channel is type:{type(jcd)}')
    jfd = json_dict['feeds'] # equals a list of dicts
    print(f'feeds is type:{type(jfd)}')
    return (jcd, jfd)


def label_feeds_dict_items_with_fieldnames(c_dict, f_dict_list):
    """Rename feeds fields with channel descriptive names.
    """
    new_list = []
    for measurement in f_dict_list:
        new_measurement = {}
        for k1, v1 in measurement.items():
            new_measurement[k1] = v1
            if k1 != 'created_at': # don't change measurement date
                if k1 in c_dict.keys(): 
                    # copy the descriptive name from the channel into the feed
                    new_measurement[c_dict[k1]] = v1
                    # remove non-descriptive entry
                    del new_measurement[k1]
        new_list.append(new_measurement)        
    return new_list


def feeds_dict_update(url):
    """Copy descriptive names of fields into feeds dict.
    """
    json_feed = load_json_data_into_dict(url)
    channel, feeds = split_dicts_from_raw_data(json_feed)
    updated_feeds = label_feeds_dict_items_with_fieldnames(channel, feeds)
    #print(updated_feeds)
    return updated_feeds


def load_data_into_pandas(list_of_dicts):
    df = pd.DataFrame(list_of_dicts)
    df = df.drop(['entry_id'], axis=1)
    df["created_at"]=pd.to_datetime(df['created_at'], format="%Y-%m-%dT%H:%M:%SZ")
    columns = list(df.columns)
    columns.remove('created_at')
    #df = df.apply(pd.to_numeric) # convert all columns of DataFrame
    # line above changes datetime obj to int64
    # convert just columns that are not 'created_at'
    df[columns] = df[columns].apply(pd.to_numeric)
    return df


def save_dataframe_to_csv(df):
    """Create permanent storage on local disk.
        Use current timestamp to organize storage.
    Args:
        df (pandas_dataframe): dataframe to be saved.
    """


def matplot_main():
    feed1 = feeds_dict_update(url1)
    feed2 = feeds_dict_update(url2)
    df1 = load_data_into_pandas(feed1)
    df2 = load_data_into_pandas(feed2)    
    print(df1)
    print(df2)    
    print(df2.dtypes)
    save_dataframe_to_csv(df1)
    ax = df2.plot.line(x='created_at')

    plt.show()
    return None

matplot_main()
