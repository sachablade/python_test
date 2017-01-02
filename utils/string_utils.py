#!/usr/bin/env python
# -*- coding: utf-8 -*-
class string_utils:
    @staticmethod
    def remove_no_printable_chars(str):
        return str.replace('\xc2\xa0', '')

    @staticmethod
    def repair_text(str):
        return str.replace('ï¿½', 'ñ')


