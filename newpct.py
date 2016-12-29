#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import pandas as pd
from my_worker import Worker
from parse_url import *

all_link_list = {}

pagination_hd = 'http:\/\/www\.newpct1\.com\/series-hd\/letter\/.*'
tag_hd='http:\/\/www\.newpct1\.com\/series-hd\/.+\/'

pagination_vo='http:\/\/www\.newpct1\.com\/series-vo\/letter\/.*'
tag_vo='http:\/\/www\.newpct1\.com\/series-vo\/.+\/'

def get_links_hd(url):
    return_link_list = []
    resp = urllib2.urlopen ( url )
    soup = BeautifulSoup ( resp,"html.parser", from_encoding=resp.info ( ).getparam ( 'charset' ) )
    for link in soup.find_all ( 'a', href=True ):
       if any(re.findall(tag_hd, link['href'])):
           if any(re.findall(pagination_hd, link['href'])) and not any(re.findall(pagination_hd, url)):
               return_link_list +=get_links_hd(link['href'])
           else:
               if not any(re.findall(pagination_hd, link['href'])):
                return_link_list.append(link['href'])
    #return_link_list = ['http://www.newpct1.com/series-hd/2-chicas-sin-blanca/2359']

    return return_link_list

def get_links_vo(url):
    return_link_list = []
    resp = urllib2.urlopen ( url )
    soup = BeautifulSoup ( resp,"html.parser", from_encoding=resp.info ( ).getparam ( 'charset' ) )
    for link in soup.find_all ( 'a', href=True ):
       if any(re.findall(tag_vo, link['href'])):
           if any(re.findall(pagination_vo, link['href'])) and not any(re.findall(pagination_vo, url)):
               return_link_list +=get_links_vo(link['href'])
           else:
               if not any(re.findall(pagination_vo, link['href'])):
                return_link_list.append(link['href'])
    return return_link_list

class ExampleMultithread (Worker):
    def __init__(self,nthreads=1):
        self.nthreads=nthreads
        self.df = pd.DataFrame(columns=['url'])
        super ( ExampleMultithread, self ).__init__ ( )

    def _retrive_task(self):
        url = 'http://www.newpct1.com/series-hd/'
        #links = get_links_hd(url)
        url = 'http://www.newpct1.com/series-vo/'
        links = get_links_vo(url)
        return links

    def _do(self,task):
        task = task.encode('utf8')
        try:
            tvshow = get_tv_info(task)
            return tvshow
        except Exception as e:
            print task, e.message



c = ExampleMultithread(10)

