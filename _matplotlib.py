#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 2.0
"""Create a plot of datapoints from ThingSpeak.
"""
from loguru import logger
import pandas as pd
import matplotlib.pyplot as plt

from _thingspeak import url_list
from _thingspeak import feeds_dict_update
from _thingspeak import load_data_into_pandas
from _thingspeak import save_dataframe_to_csv


@logger.catch
def matplot_main(urls):
    df_col_merged = pd.DataFrame()
    for url in urls:
        feed = feeds_dict_update(url)
        df = load_data_into_pandas(feed)
        print(df)
        df_col_merged = pd.concat([df_col_merged, df], axis=1)

    df_smoothed = df_col_merged.fillna(
        value=None, method="pad", axis=0, inplace=False, limit=None, downcast=None
    )

    print(df_smoothed.dtypes)
    print(df_smoothed)
    save_dataframe_to_csv(df_smoothed, "output_dir", "Filename")
    ax = df_smoothed.plot.line()  # x='created_at'

    plt.show()
    return None


matplot_main(url_list)
