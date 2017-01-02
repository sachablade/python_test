#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import pandas as pd
from page_parser.newpct_series import newpct_serie
from utils.multithread.worker import Worker
from utils.a_beautiful_soup import bs4

all_link_list = {}
pagination_hd = 'http:\/\/www\.newpct1\.com\/series-hd\/letter\/.*'
tag_hd='http:\/\/www\.newpct1\.com\/series-hd\/.+\/'

pagination_vo='http:\/\/www\.newpct1\.com\/series-vo\/letter\/.*'
tag_vo='http:\/\/www\.newpct1\.com\/series-vo\/.+\/'

def get_links_hd(url):
    return_link_list = []
    this_bs4=bs4(url)
    for link in this_bs4.get_all_links():
       if any(re.findall(tag_hd, link['href'])):
           if any(re.findall(pagination_hd, link['href'])) and not any(re.findall(pagination_hd, url)):
               return_link_list +=get_links_hd(link['href'])
           else:
               if not any(re.findall(pagination_hd, link['href'])):
                return_link_list.append(link['href'])
    #return_link_list = ['http://www.newpct1.com/series-hd/anatomia-de-grey/2259']

    return return_link_list

def get_links_vo(url):
    return_link_list = []
    this_bs4 = bs4(url)
    for link in this_bs4.get_all_links():
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
        links = get_links_hd(url)
        url = 'http://www.newpct1.com/series-vo/'
        links += get_links_vo(url)
        return list(set(links))

    def _do(self,task):
        try:
            task = task.encode('utf-8')
            #print task
            newpct_serie(task)
            return None
        except Exception as e:
            print task, e.message
            raise



c = ExampleMultithread(10)

