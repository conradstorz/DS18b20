#-*- coding: utf-8 -*-
# version 2.0
"""Create a plot of datapoints from ThingSpeak.
"""
from time import sleep, time
from loguru import logger
# import pandas as pd
import matplotlib.pyplot as plt

from _thingspeak import url_list
from _thingspeak import pandas_dataframe

import cfsiv_utils.time_strings as ts


@logger.catch
def matplot_main(urls):
    df = pandas_dataframe(urls)
    # TODO smooth data
    # EXAMPLE df = df.interpolate()
    print(f'THINGSPEAK DATA:\n{df}')
    if df.empty:
        print('No data found to plot.')
    else:
        ax = df.plot.line()
        ax.set_ylabel('Temperature')
        ax.set_title(f"Kooler Ice 410 Pearl St @ {ts.LOCAL_NOW()}")
        # print(ax)
        #plt.draw()
        plt.pause(60*60*24)
    return None


while True:
    matplot_main(url_list)
    sleep(1)
