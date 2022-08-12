import os
import re
import time
import math
import random
import statistics
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from timeit import default_timer
from numpy import unique, ravel
from numpy import array, zeros, diagonal, transpose, eye, diag, ones
from numpy import transpose, diag, dot
from numpy.linalg import svd, inv, qr, det
from matplotlib.pyplot import figure

#%%
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


from __future__ import annotations
from typing import *


def as_DataFrame(rater, pros, cons, rating):
    dd_df = {"rater": rater, "pros": pros, "cons": cons, "rating": rating}
    return pd.DataFrame(dd_df)


def JSON_to_DataFrame(json_data: dict):
    dd_ret = {'rater': [], 'pros': [], 'cons': [], 'rating': []}
    for key in json_data:
        if type(key) == int:
            for inner_key in json_data[key]:
                dd_ret[inner_key].append(json_data[key][inner_key])
    return pd.DataFrame(dd_ret)

# hacky parameter
digits = ("0", "1", "2", "3", "4", "5","6","7","8","9")


class GlassdoorReviewScrapper(object):
    
    def __init__(self, link, language_filter='?filter.iso3Language=eng'):
        self.link = link
        if '?filter' not in self.link:
            self.link = self.link + language_filter
        self.JSON_data = {}
        self.src = None
        self.soup = None
       
    def get_next_page(self):
        idx = self.link.index('.htm?')
        print(self.link[idx:])
        print(idx)
        print("\n\n NEXT PAGING")
        print(self.JSON_data)
        if self.link[idx-1] in digits:
            page_number = int(self.link[idx-1]) + 1
            return self.link[:idx-1] + str(page_number) + self.link[idx:]
        return self.link[:idx] + '_P2' + self.link[idx:]
    
    # Helps scrape
    def get_rpcr(self):
        rater = self.soup.find_all('span', attrs={"class":"middle common__EiReviewDetailsStyle__newGrey"})
        pros = self.soup.find_all('span', attrs={"data-test": "pros"})
        cons = self.soup.find_all('span', attrs={"data-test": "cons"})
        rating = self.soup.find_all('span', attrs={"class": "ratingNumber mr-xsm"})
        
        rater = [re.sub("<(.)+?>", "", str(r)) for r in rater]
        pros = [re.sub("<(.)+?>", "", str(r)) for r in pros]
        cons = [re.sub("<(.)+?>", "", str(r)) for r in cons]
        rating = [re.sub("<(.)+?>", "", str(r)) for r in rating]
        
        # add a log message
        # i.e. assert len(rater) == len(pros) == len(cons) == len(rating)
        return rater, pros, cons, rating
    
    
    def scrape(self):
        self.src = requests.get(self.link)
        self.soup = BeautifulSoup(self.src.text, 'html.parser')
        
        rater, pros, cons, rating = self.get_rpcr()
        # if any of the lists are empty
        # maybe add a log message
        if any([not lst for lst in (rater, pros, cons, rating)]):
            return self.JSON_data
        else:
            hash_idx = len(self.JSON_data)
            for r1, p, c, r2 in zip(rater, pros, cons, rating):
                self.JSON_data[hash_idx] = {"rater": r1, "pros": p, "cons": c, "rating": r2}
                hash_idx += 1
         
            # recursive call for next page
            self.link = self.get_next_page()
            self.scrape()
        return self.JSON_data


grs = GlassdoorReviewScrapper('https://www.glassdoor.com/Reviews/SynergisticIT-Reviews-E424823.htm?filter.iso3Language=eng')
data = grs.scrape()

df = JSON_to_DataFrame(grs.JSON_data)
