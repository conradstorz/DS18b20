#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 2.0
"""Retrieve datapoints from ThingSpeak.
    Also offer method to place datapoints from dataframe into CSV file storage.
"""

from loguru import logger
import requests
import pandas as pd


channel1 = "1216774"
channel2 = "1239835"
channels = [channel1, channel2]

url_str_base = "https://api.thingspeak.com/channels/"
url_str_tail = "/feeds.json?days=2"

url_list = []
for channel in channels:
    url = f"{url_str_base}{channel}{url_str_tail}"
    url_list.append(url)


@logger.catch
def load_json_data_into_dict(url):
    """Return a dict from a JSON source"""
    # TODO check for bad url response
    r = requests.get(url)
    j = r.json()
    return j


@logger.catch
def split_dicts_from_raw_data(json_dict):
    """Split channels and feeds dicts."""
    jcd = json_dict["channel"]  # equals a dict
    print(f"channel is type:{type(jcd)}")
    jfd = json_dict["feeds"]  # equals a list of dicts
    print(f"feeds is type:{type(jfd)}")
    return (jcd, jfd)


@logger.catch
def label_feeds_dict_items_with_fieldnames(c_dict, f_dict_list):
    """Rename feeds fields with channel descriptive names."""
    new_list = []
    for measurement in f_dict_list:
        new_measurement = {}
        for k1, v1 in measurement.items():
            new_measurement[k1] = v1
            if k1 != "created_at":  # don't change measurement date
                if k1 in c_dict.keys():
                    # copy the descriptive name from the channel into the feed
                    new_measurement[c_dict[k1]] = v1
                    # remove non-descriptive entry
                    del new_measurement[k1]
        new_list.append(new_measurement)
    return new_list


@logger.catch
def feeds_dict_update(url):
    """Copy descriptive names of fields into feeds dict."""
    json_feed = load_json_data_into_dict(url)
    channel, feeds = split_dicts_from_raw_data(json_feed)
    updated_feeds = label_feeds_dict_items_with_fieldnames(channel, feeds)
    return updated_feeds


@logger.catch
def load_data_into_pandas(list_of_dicts):
    df = pd.DataFrame(list_of_dicts)
    # remove "entry_id" field
    df = df.drop(["entry_id"], axis=1)
    # convert datestring to datetime object
    df["created_at"] = pd.to_datetime(df["created_at"], format="%Y-%m-%dT%H:%M:%SZ")
    columns = list(df.columns)
    columns.remove("created_at")
    # convert just columns that are not 'created_at'
    df[columns] = df[columns].apply(pd.to_numeric)
    # set 'created_at' as index
    df.set_index("created_at", inplace=True)
    return df


@logger.catch
def save_dataframe_to_csv(df, OD, FN):
    """Create permanent storage on local disk.
        Use current timestamp to organize storage.
    Args:
        df (pandas_dataframe): dataframe to be saved.
        OD (string): Directory to save file in
        FN (string): Filename to use
    """

@logger.catch
def send_tweet(tweet):
    """Uses ThingSpeak ThingTweet to send tweets.

    Args:
        tweet (Str): A valid tweet string
    """
    import urllib.request
    API_KEY = '943KI9M4I2TU316Q'
    TWEET = 'HeyWorld'
    update_url_target = f'https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key={API_KEY}&status={TWEET}'
    print(update_url_target)
    with urllib.request.urlopen(update_url_target) as response:
        html = response.read()
    return
