#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko
import time
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
ssh.connect('192.168.1.75', username='pi',password='021010')

stdin=None
stdout=None
stderr=None

file_name="'%s.torrent'"%('Gomorra - Temporada 2  [HDTV 720p][Cap.207][AC3 5.1 Español Castellano]')
torrent_url="http://tumejorjuego.com/descargar/index.php?link=descargar-torrent/1478942340_roman-empire-reign-of-blood---temporada-1--hdtv-720p-ac3-51/"

wget_command='wget -O %s %s'%(file_name,torrent_url)
trshow_s_command='transmission-show -s %s'%(file_name)
trshow_command='transmission-show %s'%(file_name)
rm_command='rm %s'%(file_name)

try:
    stdin, stdout, stderr =  ssh.exec_command(wget_command)
    time.sleep(1)
    stdin, stdout, stderr = ssh.exec_command(trshow_s_command)

    seeders=0
    leechers=0

    for item in stdout.readlines():
        seed_patterns = re.findall('(\d+) seeders, (\d+) leechers', item)
        if len(seed_patterns)>0:
            seeders += int(seed_patterns[0][0])
            leechers += int(seed_patterns[0][1])

    stdin, stdout, stderr =  ssh.exec_command(trshow_command)

    name=''
    hash=''
    total_size=''
    files=[]
    isfiles=False
    for item in stdout.readlines():
        print item
        if item.__contains__('Name: '):
            name=item.split(':')[1].encode('utf8').strip()
        if item.__contains__('Hash: '):
            hash=item.split(':')[1].encode('utf8').strip()
        if item.__contains__('Total Size: '):
            total_size=item.split(':')[1].encode('utf8').strip()
        if item == u'FILES\n':
            isfiles = True
        if isfiles and item != u'FILES\n':
            if item!= u'\n':
                files.append(item.encode('utf8').strip())

    print seeders,leechers,files
    stdin, stdout, stderr = ssh.exec_command(rm_command)


except Exception as e:
    ssh.close()
    raise

ssh.close()