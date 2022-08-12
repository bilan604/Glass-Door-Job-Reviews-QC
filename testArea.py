"""
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
from numpy import sqrt, dot, array, diagonal, mean, transpose, eye, diag, ones
from numpy import transpose, diag, dot
from numpy.linalg import svd, inv, qr, det
from sklearn.linear_model import LinearRegression
from matplotlib.pyplot import figure
"""


#%%
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


#%%
links = ['https://www.glassdoor.com/Reviews/Fast-Easy-Accounting-Reviews-E1430372.htm', \
    'https://www.glassdoor.com/Reviews/SynergisticIT-Reviews-E424823.htm']

src = requests.get(links[1])


#%%
soup = BeautifulSoup(src.text, 'html.parser')
stew = soup.prettify()


#%%
rater = soup.find_all('span', attrs={"class":"middle common__EiReviewDetailsStyle__newGrey"})
pros = soup.find_all('span', attrs={"data-test": "pros"})
cons = soup.find_all('span', attrs={"data-test": "cons"})
rating = soup.find_all('span', attrs={"class": "ratingNumber mr-xsm"})
assert len(rater) == len(pros) == len(cons) == len(rating)


#%%
rater = [re.sub("<(.)+?>", "", str(r)) for r in rater]
pros = [re.sub("<(.)+?>", "", str(r)) for r in pros]
cons = [re.sub("<(.)+?>", "", str(r)) for r in cons]
rating = [re.sub("<(.)+?>", "", str(r)) for r in rating]

#%%
dd = {}
tti = 0
for _rater,_pros,_cons,_rating in zip(rater, pros, cons, rating):
    dd[tti] = {"rater": _rater, "pros": _pros, "cons": _cons, "rating": _rating} 
    tti += 1

#%%
print(dd)