#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob,os
import pickle

files=glob.glob(os.getcwd() + "/state/*.p")

def load_pickle(file_name):
    b={}
    try:
        with open(file_name, 'rb') as handle:
            b = pickle.load(handle)
    except:
        pass
    return b


for file in files:
    try:
        tvshow=load_pickle(file)
        print tvshow['title'],len(tvshow['capitulos_list']),tvshow['capitulos']
        #if tvshow['title'] == 'Billions':
        max_name=0
        max_link=0
        for cap in tvshow['capitulos_list']:
            print len(cap['torrent_title']),cap['torrent_link'].__hash__()

    except Exception as e:
        print 'ERRROR ' + tvshow['title']
        #os.remove(file)