#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2,os
import pickle
import datetime

def slugify(value):
    try:
        import base64
        return os.getcwd()+ '/state/' + base64.urlsafe_b64encode(value)+'.p'
    except:
        print 'error base64 ' + value
        pass
def load_pickle(file_name):
    b={}
    try:
        with open(file_name, 'rb') as handle:
            b = pickle.load(handle)
    except:
        pass
    return b

def save_pickle(file_name,dict):
    with open(file_name, 'wb') as handle:
        pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def get_links_pagination(url):
    resp = urllib2.urlopen(url)
    soup = BeautifulSoup(resp, "html.parser", from_encoding=resp.info().getparam('charset'))
    pre_links = []
    for link in soup.find_all("ul", class_="buscar-list")[0].findAll('a', href=True):
        pre_links.append(link['href'].encode('utf-8'))
    return pre_links

def get_torrent_info(url):
    torrent_info={}
    resp = urllib2.urlopen(url)
    torrent_info['url']=url

    soup = BeautifulSoup(resp, "html.parser", from_encoding=resp.info().getparam('charset'))

    torrent_title=soup.find_all("div", class_="page-box")[0].find('h1').text.encode('latin1').split('/')[1]
    torrent_info['torrent_title']=torrent_title[2:].decode('latin1')
    for link in soup.find_all("span", class_="imp"):
        if link.text.find('Size:') != -1:
            torrent_info['size']=[link.text.split(' ')[1].encode('utf-8'),link.text.split(' ')[2].encode('utf-8')]
        if link.text.find('Fecha:') != -1:
            try:
                torrent_info['date']=link.text.split(' ')[1].encode('utf-8')
            except:
                torrent_info['date'] = None
                pass

    tab1=soup.find("div", {"id": "tab1"})
    try:
        for link in tab1.find_all("a", href=True):
            torrent_info['torrent_link']=link['href'].decode('latin1')
    except:
        print 'Error en: ' + url


    return torrent_info

def get_tv_info(url):
    print 'Buscando en ' + url
    file_name=slugify(url)
    tvshow=load_pickle(file_name)

    resp = urllib2.urlopen(url)
    soup = BeautifulSoup(resp, "html.parser", from_encoding=resp.info().getparam('charset'))

    tvshow['url'] = url
    tvshow['update']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cap=0
    capitulos = soup.find_all("div", class_="page-box")[1].findAll('strong')[0].text
    cap = int(capitulos.split(" ")[1])

    buscar_capitulos=True
    if tvshow.has_key('capitulos'):
        if tvshow['capitulos']==cap:
            buscar_capitulos = False

    tvshow['capitulos']=cap
    if buscar_capitulos:
        title=soup.find_all("ul", class_="breadcrumbs")[0].findAll('a', href=True)
        tvshow['title'] = str(title[len(title)-1].text.encode('utf-8')).strip()

        for link in soup.find_all("div", class_="entry-left")[0].findAll('img'):
            tvshow['picture']=link['src'].encode('utf-8')
        pagination = []
        try:
            for link in soup.find_all("ul", class_="pagination")[0].findAll('a', href=True):
                pagination.append(link['href'].encode('utf-8'))
            pagination = sorted(list(set(pagination)))
        except:
            pass
        pre_links = []
        for link in soup.find_all("ul", class_="buscar-list")[0].findAll('a', href=True):
            pre_links.append(link['href'].encode('utf-8'))

        for pag in pagination[1:]:
            pre_links+=get_links_pagination(pag)
        pre_links=list(set(pre_links))

        capitulos = []
        for link in pre_links:
            capitulos.append(get_torrent_info(link))

        tvshow['capitulos_list']=capitulos
        save_pickle(file_name,tvshow)

    print 'Finalizando ' + url

    return tvshow


