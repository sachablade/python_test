#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import re
import pandas as pd
from my_worker import Worker
from parse_url import *

all_link_list = {}

pagination = 'http:\/\/www\.newpct1\.com\/series-hd\/letter\/.*'
tag='http:\/\/www\.newpct1\.com\/series-hd\/.+\/'

pag_serie='http:\/\/www\.newpct1\.com\/serie.*\/##TEXT##.*\/\d.*\/pg.*'
capitulo='http:\/\/www\.newpct1\.com\/serie\/##TEXT##.*\/capi.*'

def get_links(url):

    return_link_list = []
    resp = urllib2.urlopen ( url )
    #print resp.info().getparam('charset' )
    soup = BeautifulSoup ( resp,"html.parser", from_encoding=resp.info ( ).getparam ( 'charset' ) )
    for link in soup.find_all ( 'a', href=True ):
       if any(re.findall(tag, link['href'])):
           if any(re.findall(pagination, link['href'])) and not any(re.findall(pagination, url)):
               return_link_list +=get_links(link['href'])
           else:
               if not any(re.findall(pagination, link['href'])):
                return_link_list.append(link['href'])

    '''return_link_list = ['http://www.newpct1.com/series-hd/el-pequeño-quinquin/2018','http://www.newpct1.com/series-hd/la-extraña-pareja/2745']
    '''

    return return_link_list

def get_links_generic(df, url ,match, pagination):
    return_link_list = []
    resp = urllib2.urlopen ( url )
    soup = BeautifulSoup ( resp,"html.parser", from_encoding=resp.info ( ).getparam ( 'charset' ) )
    for link in soup.find_all ('a', href=True):
        if any ( re.findall ( pagination, link['href'])) and not any (re.findall( pagination, url )):
            if not link['href'] in df['url'].tolist():
                df.loc[len ( df )] = [link['href']]
                return_link_list += get_links_generic(df,link['href'],match,pagination)
        else:
            if any ( re.findall (match, link['href'] )):
                if not link['href'] in df['url'].tolist ( ):
                    df.loc[len ( df )] = [link['href']]
                    return_link_list.append (link['href'])
    return return_link_list

class ExampleMultithread (Worker):
    def __init__(self,nthreads=1):
        self.nthreads=nthreads
        self.df = pd.DataFrame(columns=['url'])
        super ( ExampleMultithread, self ).__init__ ( )

    def _retrive_task(self):
        url = 'http://www.newpct1.com/series-hd/'
        return get_links (url )

    def _do(self,task):
        task = task.encode('utf8')
        try:

            tvshow = get_tv_info(task)
            return tvshow
        except:
            print task

        '''resp = urllib2.urlopen ( task )
        soup = BeautifulSoup ( resp, "html.parser", from_encoding=resp.info ( ).getparam ( 'charset' ))
        text= task.split("/")[4]
        self.df.loc[len(self.df)]=[task]
        links = get_links_generic(self.df, task,capitulo.replace("##TEXT##",text), pag_serie.replace("##TEXT##",text))
        download_links=[]
        for row in links:
            download_links+=get_links_generic(self.df, row ,'descarga-torrent.*', 'aslhdñasdhña')

        print download_links
        print str(task) +'|'+ str(len(self.df))
        return str(task) +'|'+ str(len(self.df))'''



c = ExampleMultithread(10)

