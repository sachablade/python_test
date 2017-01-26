#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from utils.a_beautiful_soup import bs4
from utils.string_utils import string_utils
from utils.json_utils import utils_json


class newpct_page( utils_json):
    def __init__(self, url):
        super(newpct_page, self).__init__()
        self.url = url
        self.bs4 = bs4(url)
        self.id = url.__hash__()
        self.get_info()
        self.bs4 = None

    def get_info(self):
        # Obtenemos el título
        try:
            torrent_title = self.bs4.soup.find_all("div", class_="page-box")[0].find('h1').text.encode('latin1').split(
                '/')
            if len(torrent_title) > 1:
                self.title = string_utils.remove_no_printable_chars(
                    torrent_title[1].decode('iso-8859-1').encode('utf8'))
            else:
                self.title = string_utils.remove_no_printable_chars(
                    torrent_title[0].decode('iso-8859-1').encode('utf8'))
        except Exception as e:
            self.title = None
        # Obtenemos el tamaño y la fecha de publicación
        try:
            for link in self.bs4.soup.find_all("span", class_="imp"):
                if link.text.find('Size:') != -1:
                    try:
                        size = float(link.text.split(' ')[1].encode('utf-8'))
                        self.size = 0.0 if math.isnan(size) else size
                        self.unit = link.text.split(' ')[2].encode('utf-8')
                    except Exception as e:
                        self.size = 0.0
                        self.unit = ''

                if link.text.find('Fecha:') != -1:
                    try:
                        self.date = link.text.split(' ')[1].encode('utf-8')
                    except Exception as e:
                        self.date = None

        except Exception as e:
            self.size = 0.0
            self.unit = ''

        '''try:
            self.plot=self.bs4.soup.find("div", class_="sinopsis").text.decode('iso-8859-1').encode('utf8')
        except Exception as e:
            self.plot = None

        try:
            self.plot_description=self.bs4.soup.find("div", class_="descripcion_top").text.decode('iso-8859-1').encode('utf8')
        except Exception as e:
            self.plot_description = None'''

        try:
            tab1 = self.bs4.soup.find("div", {"id": "tab1"})
            for link in tab1.find_all("a", href=True):
                self.torrent_link = str(link['href'])
        except Exception as e:
            self.torrent_link = None


if __name__ == '__main__':
    obj = newpct_page('http://www.newpct1.com/serie/el-pequeno-quinquin/capitulo-102/')
    obj.get_info()
    print obj
    obj = newpct_page('http://www.newpct1.com/descargar-pelicula/no-respires/blurayrip-ac3-5-1/')
    obj.get_info()
    print obj
