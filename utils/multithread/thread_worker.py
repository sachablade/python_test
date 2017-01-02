# -*- coding: utf-8 -*-
import threading

class ThreadWorker():
    def __init__(self,func):
        self.thread = None
        self.data = None
        self.func = self.save_data(func)

    def save_data(self,func):
        def new_func(*args, **kwargs):
            self.data=func(*args, **kwargs)
        return new_func

    def start(self):
        self.data = None
        if self.thread is not None:
            if self.thread.isAlive():
                return 'running'
        self.thread = threading.Thread(target=self.func)
        self.thread.start()
        return 'started'

    def status(self):
        if self.thread is None:
            return 'not_started'
        else:
            if self.thread.isAlive():
                return 'running'
            else:
                return 'finished'

    def get_results(self):
        if self.thread is None:
            return 'not_started' #could return exception
        else:
            if self.thread.isAlive():
                return 'running'
            else:
                return self.data

