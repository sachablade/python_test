#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from utils.a_beautiful_soup import bs4
from utils.json_utils import utils_json


class filmaffinity_page(utils_json):
    def __init__(self, url):
        self.url = url
        self.bs4 = bs4(url)
        id = re.findall('\d+', url)
        self.id = id[0]
        self.get_info()
        self.bs4 = None
        super(filmaffinity_page,self ).__init__()

    def get_info(self):
        # Obtenemos el título
        try:
            self.Title=self.bs4.soup.find("span", itemprop="name").text.encode('utf8')
        except Exception as e:
            self.Title=None

        try:
            self.Year=self.bs4.soup.find("dd", itemprop="datePublished").text.encode('utf8')
        except Exception as e:
            self.Year=None

        try:
            self.Runtime=self.bs4.soup.find("dd", itemprop="duration").text.encode('utf8')
        except Exception as e:
            self.Runtime=None

        try:
            Genres=self.bs4.soup.find_all("span", itemprop="genre")
            tmp=[]
            for i in range(len(Genres)):
                tmp.append(Genres[i].text.encode('utf8'))
            self.Genre=tmp
        except Exception as e:
            self.Genre=[]

        try:
            Director = self.bs4.soup.find_all("span", itemprop="director")
            tmp = []
            for i in range(len(Director)):
                tmp.append(Director[i].find("span", itemprop="name").text.encode('utf8'))
            self.Director = tmp
        except Exception as e:
            self.Director = []

        try:
            Actors = self.bs4.soup.find_all("span", itemprop="actor")
            tmp = []
            for i in range(len(Actors)):
                tmp.append(Actors[i].find("span", itemprop="name").text.encode('utf8'))
            self.Actors = tmp
        except Exception as e:
            self.Actors = []

        try:
            Plot=self.bs4.soup.find("dd", itemprop="description").text.encode('utf8')
            Plot=''.join(Plot.splitlines())
            serie_patterns=re.findall('(Serie de TV\.* \((\d{4})-(\w+)\)\. )', Plot)
            if len(serie_patterns[0])==3:
                if serie_patterns[0][0].startswith("Serie de TV"):
                    self.Plot=Plot.replace(serie_patterns[0][0],'').replace('\\n','')
                    print self.Plot
                    self.Year=serie_patterns[0][1] + '-' + serie_patterns[0][2]
                    self.Type='series'
        except Exception as e:
            self.Plot=None
            self.Type=None

        try:
            self.Country=self.bs4.soup.find("span", id="country-img").find("img")['alt'].encode('utf8')
        except Exception as e:
            self.Country=None

        try:
            self.Rating=self.bs4.soup.find("div", id="movie-rat-avg")['content'].encode('utf8')
        except Exception as e:
            self.Rating=None

        try:
            self.Poster=self.bs4.soup.find("img", itemprop="image")['src'].encode('utf8')
        except Exception as e:
            self.Poster=None


if __name__ == '__main__':
    obj = filmaffinity_page('http://www.filmaffinity.com/es/film874956.html')
    print obj

