#-*- coding: utf-8 -*-
# version 2.0
"""Create a plot of datapoints from ThingSpeak.
"""
from loguru import logger
import pandas as pd
import matplotlib.pyplot as plt

from _thingspeak import url_list
from _thingspeak import pandas_dataframe

import cfsiv_utils.filehandling as fh

@logger.catch
def matplot_main(urls):
    df = pandas_dataframe(urls)
    if df.empty:
        print('No data found to plot.')
    else:
        ax = df.plot.line()
        print(ax)
        plt.show()
    return None


matplot_main(url_list)
