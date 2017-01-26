#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import time
from datetime import datetime
from utils.json_utils import utils_json


class torrent_info(utils_json):
    def __init__(self,cap,ssh):
        super(torrent_info, self).__init__()
        self.cap=cap
        file_path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__)), os.pardir)) + '/state/torrent_info/%s.json' % self.cap['id']
        self.json = self.readJSONfile(file_path)
        self.get_info(ssh)


    def get_info(self,ssh):
            self.update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.json is None:
                if self.cap.has_key('torrent_link'):
                    print self.cap['title']
                    file_name = "'%s.torrent'" % (self.cap['title'])
                    torrent_url = self.cap['torrent_link']

                    wget_command = 'wget -O %s %s' % (file_name, torrent_url)
                    trshow_s_command = 'transmission-show -s %s' % (file_name)
                    trshow_command = 'transmission-show %s' % (file_name)
                    rm_command = 'rm %s' % (file_name)

                    try:
                        stdin, stdout, stderr = ssh.exec_command(wget_command)
                        time.sleep(1)
                        stdin, stdout, stderr = ssh.exec_command(trshow_s_command)

                        self.seeders = 0
                        self.leechers = 0

                        for item in stdout.readlines():
                            seed_patterns = re.findall('(\d+) seeders, (\d+) leechers', item)
                            if len(seed_patterns) > 0:
                                self.seeders += int(seed_patterns[0][0])
                                self.leechers += int(seed_patterns[0][1])

                        stdin, stdout, stderr = ssh.exec_command(trshow_command)

                        self.files = []
                        isfiles = False
                        for item in stdout.readlines():
                            if item.__contains__('Name: '):
                                self.name = item.split(':')[1].encode('utf8').strip()
                            if item.__contains__('Hash: '):
                                self. hash = item.split(':')[1].encode('utf8').strip()
                            if item.__contains__('Total Size: '):
                                self.total_size = item.split(':')[1].encode('utf8').strip()
                            if item == u'FILES\n':
                                isfiles = True
                            if isfiles and item != u'FILES\n':
                                if item != u'\n':
                                    self.files.append(item.encode('utf8').strip())

                        stdin, stdout, stderr = ssh.exec_command(rm_command)

                        if len(self.files)>0:
                            file_path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__)),os.pardir)) + '/state/torrent_info/%s.json' % self.cap['id']
                            self.toJSONfile(file_path)

                    except Exception as e:
                        raise


if __name__ == '__main__':
    obj=torrent_info('C:\Workspaces\pythonSpaces\python_test/state/newpct_series\-1002933835.json')

