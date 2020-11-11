#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request

API_KEY = '943KI9M4I2TU316Q'
TWEET = 'HeyWorld'
update_url_target = f'https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key={API_KEY}&status={TWEET}'


print(update_url_target)
with urllib.request.urlopen(update_url_target) as response:
    html = response.read()