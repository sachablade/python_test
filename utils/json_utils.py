#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from utils.string_utils import string_utils

class utils_json(object):
    def __repr__(self):
        return self.toJSON()

    def __init__(self):
        pass

    def toDICT(self):
        items = [[k, v] for k, v in self.__dict__.items()]
        itemsdict = {}
        for item in items:
            if type(item[1]) is str or type(item[1]) is int or type(item[1]) is bool or type(item[1]) is float:
                itemsdict[item[0]] = item[1]
            if type(item[1]) is list:
                listdict=[]
                for i in item[1]:
                    if type(i) is str or type(i) is int or type(i) is bool or type(i) is float:
                        listdict.append(i)
                    else:
                        listdict.append(i.toDICT())
                itemsdict[item[0]] = listdict
        return itemsdict

    def toJSON(self):
        itemsdict=self.toDICT()
        return string_utils.repair_text(json.dumps(itemsdict).decode('unicode-escape').encode('utf8'))

    def toJSONfile(self,path):
        json=self.toJSON()
        text_file = open(path, "w")
        text_file.write(json)
        text_file.close()

    @staticmethod
    def readJSONfile(path):
        try:
            with open(path) as data_file:
                data = json.load(data_file)
            return data
        except:
            return None