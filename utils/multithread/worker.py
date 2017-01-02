# -*- coding: utf-8 -*-
import sys
from Queue import Queue,Empty
from thread_worker import ThreadWorker

class Worker(object):
    myQueue=None
    def retrive_task_worker(self):
        try:
            list = self._retrive_task()
            [self.myQueue.put(x) for x in list]
            print 'se han leido:', str(len(list)), 'elementos'
        except Exception as e:
            raise Exception, "%s" % e, sys.exc_info ( )[2]

    def worker(self):
        list = []
        try:
            while not self.myQueue.empty ( ):
                item = self.myQueue.get_nowait ( )
                rtn_data = self._do(item)
                if rtn_data is not None:
                    list.append (rtn_data)
        except Empty:
            return list
        return list

    def __init__(self):
        super ( Worker, self ).__init__ ( )
        self.myQueue = Queue ( )
        self.retrive_task_worker()
        n = self.nthreads
        threads = [None] * n
        for i in range ( len ( threads ) ):
            threads[i] = ThreadWorker(self.worker)
            threads[i].start()

        status=True
        while status:
            status = False
            for i in range (len ( threads ) ):
                if threads[i].status()=='running':
                    status = True

        for i in range ( len ( threads ) ):
            result = threads[i].get_results ( )
            if result is not None:
                if len(result)>0:
                    print result




