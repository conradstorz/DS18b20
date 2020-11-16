#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
# use thingspeak to tweet
"""
API_KEY = '943KI9M4I2TU316Q'
TWEET = 'HeyWorld'
update_url_target = f'https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key={API_KEY}&status={TWEET}'


print(update_url_target)
with urllib.request.urlopen(update_url_target) as response:
    html = response.read()
print(html)
"""

# use thingspeak to record data from raspberryPi
"""
You can use your web browser to complete GET HTTP requests to the RESTful API for ThingSpeak™.

Copy the URL to the address bar of your web browser, changing <write_api_key> to your user API Key, which is found in Account > My Profile.

https://api.thingspeak.com/update.json?api_key=<write_api_key>&field1=123

The response is a JSON object of the new entry, and a 200 OK from the server.

{
    "channel_id": 266256,
    "created_at": "2018-09-10T17:41:59Z",
    "entry_id": 2,
    "field1": "123",
    "field2": null,
    "field3": null,
    "field4": null,
    "field5": null,
    "field6": null,
    "field7": null,
    "field8": null,
    "latitude": null,
    "longitude": null,
    "elevation": null,
    "status": null
}

"""


# get data from ThingSpeak in JSON format
"""
https://api.thingspeak.com/channels/9/feeds.json?start=2011-11-11%2010:10:10&end=2011-11-11%2011:11:11

JSON Example

GET https://api.thingspeak.com/channels/9/feeds.json?results=2
or GET https://api.thingspeak.com/channels/9/feeds?results=2

The response is a JSON object of the channel feed, for example:

{
"channel": {
"id": 9,
"name": "my_house",
"description": "Netduino Plus connected to sensors around the house",
"latitude": "40.44",
"longitude": "-79.9965",
"field1": "Light",
"field2": "Outside Temperature",
"created_at": "2010-12-14T01:20:06Z",
"updated_at": "2018-01-26T13:08:04Z",
"last_entry_id": 13633195
},
"feeds": [
{
"created_at": "2018-01-26T13:07:48Z",
"entry_id": 13633194,
"field1": "150",
"field2": "23.014861995753716"
},
{
"created_at": "2018-01-26T13:08:04Z",
"entry_id": 13633195,
"field1": "142",
"field2": "23.86411889596603"
}
]
}
"""