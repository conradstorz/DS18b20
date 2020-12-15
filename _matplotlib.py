#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 2.0
"""Create a plot of datapoints from ThingSpeak.
"""
from loguru import logger
import pandas as pd
import matplotlib.pyplot as plt

from _thingspeak import url_list
from _thingspeak import pandas_dataframe


@logger.catch
def matplot_main(urls):
    df = pandas_dataframe(urls)
    ax = df.plot.line()
    plt.show()
    return None


matplot_main(url_list)
