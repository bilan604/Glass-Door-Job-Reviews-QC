import os
import re
import time
import numpy as np
import pandas as pd


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


from __future__ import annotations
from typing import *

# the bot
from ReviewBot import GlassdoorReviewScrapper

# from JSON format to a pandas DataFrame
def JSON_to_DataFrame(json_data: dict):
    dd_ret = {'rater': [], 'pros': [], 'cons': [], 'rating': []}
    for key in json_data:
        if type(key) == int:
            for inner_key in json_data[key]:
                dd_ret[inner_key].append(json_data[key][inner_key])
    return pd.DataFrame(dd_ret)

# creates a python dictionary that can be directly turned into a pandas dataframe
def as_dd(json_data: dict):
    dd_ret = {'rater': [], 'pros': [], 'cons': [], 'rating': []}
    for key in json_data:
        if type(key) == int:
            for inner_key in json_data[key]:
                dd_ret[inner_key].append(json_data[key][inner_key])
    return dd_ret

# use export_as_txt("text_file_name.txt") to export
def export_as_txt(file_name):
    dd_export = as_dd(grs.JSON_data)
    with open(file_name, "w+") as f:
        f.write( ", ".join([str(k) for k in dd_export.keys()]) + '\n')
        export = list(dd_export.values())
        for r1, p, c, r2 in zip(export[0], export[1], export[2], export[3]):
            f.write(", ".join([str(item) for item in (r1,p,c,r2)]) + '\n')
        f.close()
    return None

# creates a DataFrame; outdated
def as_DataFrame(rater, pros, cons, rating):
    dd_df = {"rater": rater, "pros": pros, "cons": cons, "rating": rating}
    return pd.DataFrame(dd_df)

"""
Usage Examples:
"""

# webscrapping:
grs = GlassdoorReviewScrapper('https://www.glassdoor.com/Reviews/SynergisticIT-Reviews-E424823.htm?filter.iso3Language=eng')
grs.scrape()

# creating a pandas DataFrame of reviews
df = JSON_to_DataFrame(grs.JSON_data)
