import requests
import pandas as pd
import matplotlib.pyplot as plt
#from votes import wide as df
url_str = 'https://api.thingspeak.com/channels/1216774/feeds.json?days=2'

def load_data(nrows):
    r = requests.get(url_str)
    j = r.json()
    df = pd.DataFrame(j['feeds'])
    df = df.drop(['entry_id'], axis=1)
    df["created_at"]=pd.to_datetime(df['created_at'], format="%Y-%m-%dT%H:%M:%SZ")
    #df = df.apply(pd.to_numeric) # convert all columns of DataFrame
    # line above changes datetime obj to int64
    # convert just columns "field1", 'field2', 'field3', 'field4' and "field5"
    field_list = ['field1', 'field2', 'field3', 'field4', 'field5']
    df[field_list] = df[field_list].apply(pd.to_numeric)
    return df

df = load_data(10000)
print(df)
print(df.dtypes)
ax = df.plot.line(x='created_at')

plt.show()