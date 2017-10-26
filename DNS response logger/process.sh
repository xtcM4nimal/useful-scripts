#!/bin/bash
ls -t /tmp/dns.pcap* | tail -n +2 | xargs -I {} /root/dns_logs/tocsv.py {}
chown cloud:cloud /home/cloud/logs/*
