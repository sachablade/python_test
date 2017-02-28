#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
from utils.a_beautiful_soup import bs4
from utils.json_utils import utils_json
from page_parser.newpct_page import newpct_page

class newpct_serie(utils_json):
    def __init__(self,url):
        self.url=url
        self.bs4=bs4(url)
        self.id=url.__hash__()

        file_path = os.path.abspath(
            os.path.join(os.path.join(os.path.dirname(__file__)), os.pardir)) + '/state/newpct_series/%s.json' % self.id
        self.json=self.readJSONfile(file_path)

        self.get_info()
        self.bs4 = None

    def get_links_pagination(self,url):
        this_bs4=bs4(url)
        pre_links = []
        for link in this_bs4.soup.find_all("ul", class_="buscar-list")[0].findAll('a', href=True):
            pre_links.append(link['href'].encode('utf-8'))
        return pre_links

    def get_info(self):
        self.update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.capitulos = self.bs4.soup.find_all("div", class_="page-box")[1].findAll('strong')[0].text
            self.capitulos=int(self.capitulos.split(" ")[1])
        except Exception as e:
            self.capitulos=None
        #Obtenemos el título de la serie

        '''try:
            self.plot = self.bs4.soup.find("div", class_="sinopsis").text.encode('utf8')
        except Exception as e:
            self.plot = None

        try:
            self.plot_description = self.bs4.soup.find("div", class_="descripcion_top").text.encode('utf8')
        except Exception as e:
            self.plot_description = None'''

        buscar_capitulos = True
        if self.json is not None:
            if self.json['capitulos'] == self.capitulos:
                buscar_capitulos = False

        if buscar_capitulos:
            try:
                title = self.bs4.soup.find_all("ul", class_="breadcrumbs")[0].findAll('a', href=True)
                self.title = str(title[len(title) - 1].text.encode('utf-8')).strip()
            except Exception as e:
                self.title=None
            #Obtenemos la imagen
            print self.title
            try:
                for link in self.bs4.soup.find_all("div", class_="entry-left")[0].findAll('img'):
                    self.image = link['src'].encode('utf-8')
            except Exception as e:
                self.image = None
            #Obtengo la paginación para buscar enlaces
            try:
                pagination = []
                for link in self.bs4.soup.find_all("ul", class_="pagination")[0].findAll('a', href=True):
                    pagination.append(link['href'].encode('utf-8'))
                pagination = sorted(list(set(pagination)))
            except Exception as e:
                pagination=[]

            #Busco los enlaces de la serie
            pre_links = []
            try:
                for link in self.bs4.soup.find_all("ul", class_="buscar-list")[0].findAll('a', href=True):
                    pre_links.append(link['href'].encode('utf-8'))

                for pag in pagination[1:]:
                    pre_links += self.get_links_pagination(pag)
                pre_links = list(set(pre_links))
            except Exception as e:
                pre_links = []

            #Obtengo la información de torrent
            try:
                capitulos = []
                for link in pre_links:
                    cap=newpct_page(link)
                    capitulos.append(cap)
                self.capitulos_list=capitulos
            except Exception as e:
                self.capitulos_list=[]

            file_path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__)),os.pardir)) + '/state/newpct_series/%s.json' % self.id
            self.toJSONfile(file_path)


if __name__ == '__main__':
    obj=newpct_serie('http://www.newpct1.com/series-hd/el-pequeño-quinquin/2018')
    obj=newpct_serie('http://www.newpct1.com/series/halt-and-catch-fire/1884')
