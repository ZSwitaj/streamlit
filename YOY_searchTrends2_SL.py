# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 14:48:54 2020

@author: zswitaj
"""
import pandas as pd
import YOY_searchTrends_SL as trends

kw_dict = {
    "Timberland": "/m/05kv16",
    "Timberland Boots": "Timberland Boots",
    "UGG": "/m/06wccjq",
    "Dr Martens": "/m/01lsm6",
    "Merrell": "/m/0kqrz3",
    "The North Face": "/m/04n92b",
    "Patagonia": "/m/0g152j",
    "Allbirds": "/g/11g6j4k3hl",
    "Vans": "/m/04kbwy",
    "Amazon": "/m/0mgkg ",
    "Walmart": "/m/0841v",
    "Target": "/m/01b39j",
    "Zappos": "/m/02dfb9",
    "Foot Locker": "/m/08fhy9",
    "Journeys": "/m/03cbgd",
    "DSW": "/m/0flp70",
    "Nordstrom": "/m/01fc_q",
    "Macy's": "/m/01pkxd ",
    "REI": "/m/02nx4d",
    "Dick's Sports": "/m/06fgv_",
    "Boot": "/m/01b638",
    "Outerwear": "Outerwear"
    }

lst_keywords = []

print("Adding keywords...")
for topic in kw_dict:
    lst_keywords.append(topic)

lst_values = []

for topic in kw_dict:
    print("Calculting {} results".format(topic))
    lst_values.append(round(trends.getTrendData(kw_dict[topic]),1))

print("Combining...")
res = dict(zip(lst_keywords, lst_values))
res_df = pd.DataFrame.from_dict(res, orient = 'index', columns = ['YOY Change'])
res_df = res_df.transpose()

# res_df.to_csv(r'output.csv')
