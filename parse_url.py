#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2


url='http://www.newpct1.com/series-hd/2-chicas-sin-blanca/2359'

resp = urllib2.urlopen ( url )
soup = BeautifulSoup ( resp,"html.parser", from_encoding=resp.info ( ).getparam ( 'charset' ))

print soup
for link in soup.find_all("ul", class_="breadcrumbs")[0].findAll('a',href=url):
    print link.contents

