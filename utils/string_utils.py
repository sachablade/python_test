#!/usr/bin/env python
# -*- coding: utf-8 -*-
class string_utils:
    @staticmethod
    def remove_no_printable_chars(str):
        strReturn=str.replace('\xc2\xa0', '')
        strReturn=strReturn.replace('\t', ' ')
        return strReturn

    @staticmethod
    def repair_text(str):
        return str.replace('ï¿½', 'ñ')


