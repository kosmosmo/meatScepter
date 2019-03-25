from bs4 import BeautifulSoup
import urllib2
import json,os

class meatFactory():
    def __init__(self,keys):
        self.keys = keys
        self.res = []

    def get_soup(self,url, header):
        return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)), 'html.parser')

    def main(self):
        for query in self.keys:
            query = query.split()
            query = '+'.join(query)
            url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
            header = {
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
            soup = self.get_soup(url, header)
            for a in soup.find_all("div", {"class": "rg_meta"}):
                link= json.loads(a.text)["ou"]
                self.res.append(link)

    def cache(self):
        self.main()
        print len(self.res)
        with open('CacheUrl.txt', 'w') as outfile:
            json.dump(self.res, outfile)

#keys = ["cat"]
keys = ["cock dick", "cock penis", "cock big", "cock small","cock cum"]
a = meatFactory(keys).cache()