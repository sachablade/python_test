#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import timedelta

class datetime_utils:
    @staticmethod
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

