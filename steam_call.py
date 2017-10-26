#!/usr/bin/python

# Purpose: Returns IDs from a local steam caching server's logs.
import os, sys

steam_ids_fd = os.popen('''
awk '/GET/ {print$7}' /data/www/logs/lancache-steam-access.log | awk -F"/" '{print$3}' | sort | uniq
''','r')
steam_ids=[]
for line in steam_ids_fd:
  steam_ids.append(line.strip())
steam_ids_fd.close()

# Uses the Steam IDs to retrieve friendly titles
steam_title={}
for i in steam_ids:
  curl_fd = os.popen('''
		curl -v --silent https://steamdb.info/app/%s/ --stderr -  | grep name | grep "td itemprop" | awk -F">" '{print$2}' | awk -F"<" '{print$1}';
	''' % ( i ), 'r' )
  for line in curl_fd:
    steam_title[i] = line.strip()

print steam_title