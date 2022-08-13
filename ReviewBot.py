class GlassdoorReviewScrapper(object):
    
    def __init__(self, link: str, language_filter='?filter.iso3Language=eng'):
        self.link = link
        if '?filter' not in self.link:
            self.link = self.link + language_filter
        
        self.JSON_data = {}
        self.src = None
        self.soup = None
    
    # helper function for scrape()
    def get_next_page(self):
        idx = self.link.index('.htm?')
        
        # if this is the first page
        if '_' not in self.link[idx-5: idx]:
            self.link= self.link[:idx] + '_P2' + self.link[idx:]
        else:
            page_number = int(self.link[idx-1]) + 1
            self.link = self.link[:idx-1] + str(page_number) + self.link[idx:]
    
    # helper function for scrape()
    def get_rpcr(self):
        rater = self.soup.find_all('span', attrs={"class":"middle common__EiReviewDetailsStyle__newGrey"})
        rater = [re.sub("<(.)+?>", "", str(r)) for r in rater]
        
        pros = self.soup.find_all('span', attrs={"data-test": "pros"})
        pros = [re.sub("<(.)+?>", "", str(r)) for r in pros]
        
        cons = self.soup.find_all('span', attrs={"data-test": "cons"})
        cons = [re.sub("<(.)+?>", "", str(r)) for r in cons]
        
        rating = self.soup.find_all('span', attrs={"class": "ratingNumber mr-xsm"})
        rating = [re.sub("<(.)+?>", "", str(r)) for r in rating]
        
        return rater, pros, cons, rating

    # main function
    def scrape(self, tryLimit=3):
        if tryLimit == 0:
            return self.JSON_data

        self.src = requests.get(self.link)

        # sleep so that the page can fully load (without a web-driver)
        time.sleep(8)
        
        self.soup = BeautifulSoup(self.src.text, 'html.parser')

        rater, pros, cons, rating = self.get_rpcr()

        if any([not lst for lst in (rater, pros, cons, rating)]):
            self.scrape(tryLimit - 1)
        else:
            hash_idx = len(self.JSON_data)
            for r1, p, c, r2 in zip(rater, pros, cons, rating):
                self.JSON_data[hash_idx] = {"rater": r1, "pros": p, "cons": c, "rating": r2}
                hash_idx += 1

            # change the link
            self.get_next_page()
            
            # more sleeping
            time.sleep(6)
            
            # recursive call for next page
            self.scrape()
        return self.JSON_data
