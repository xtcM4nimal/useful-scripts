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

print steam_ids