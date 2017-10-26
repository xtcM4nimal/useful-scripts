#!/usr/bin/python

import os, sys

steam_ids_fd = os.popen('''
awk '/GET/ {print$7}' /data/www/logs/lancache-steam-access.log | awk -F"/" '{print$3}' | sort | uniq
''','r')
steam_ids=[]
for line in steam_ids_fd:
  steam_ids.append(line.strip())
steam_ids_fd.close()

#curl -v --silent https://steamdb.info/app/50300/ --stderr -  | grep name | grep "td itemprop" | awk -F">" '{print$2}' | awk -F"<" '{print$1}'
#awk '/GET/ {print$7}' /data/www/logs/lancache-steam-access.log | awk -F"/" '{print$3}' | sort | uniq | wc -l

print steam_ids