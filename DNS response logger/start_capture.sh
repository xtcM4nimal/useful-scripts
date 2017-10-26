#!/bin/bash
#Get this servers IP
IP=`/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'`
DATE=`date +%Y-%m-%d-%H:%M:%S`
#Get the PID of the old running tcpdump
PID=`ps aux | grep tcpdump | grep $IP | grep -v grep | tail -n1 | awk '{print $2}'`
#When we kill it (-SIGINT) is the same as ctrl-C
#It will rotate out, and we can grab the old one
#echo PID
#echo $PID
#If $PID is not empty, kill it
if [ ! -z "$PID" ]; then
  kill -SIGINT $PID
fi
/usr/sbin/tcpdump -tttt -K -i eth0 -vvv -s 0 -l -n src host $IP and src port 53 > /tmp/dns.pcap-$DATE &2>>/tmp/tcpdumpError
