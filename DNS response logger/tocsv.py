#!/usr/bin/python
import datetime
import itertools
import shutil
import csv
import sys
import os
fname=sys.argv[1]
curDate = datetime.datetime.now().date()
curTime = datetime.datetime.now().time()
outputArr = []#[["time","realIP","queryType","queriedDomain","results"]]
with open(fname) as f:
#at some time, test that it starts with a date for line1
    for line1,line2 in itertools.izip_longest(*[f]*2):
	time = line1[:19]+"+02:00"
	if line2 and not "ServFail" in line2:


	    clipped = line2.split("> ",1)[1]
	    ipport = clipped.split(":",1)[0]
	    realIP = ipport.rsplit(".",1)[0]
	    query = clipped.split("q: ",1)
	    if (len(query)!=1):
		queryType = query[1].rsplit("? ",1)
		if (queryType[0] == "A"):
#		    print "queryType"
#		    print queryType
		    queriedDomain = queryType[1].split(". ")[0]
		    reply = queryType[1].split(" A ")
		    cname = 0

		    resultIP=""
		    if len(reply)!=1:
#			print "reply"
			count = 0
			for block in reply:
			    if count == 1:
#				print block
				IP = block.split(" ")[0]
				IP = IP.split(",")[0]
				if resultIP != "":
				    resultIP = resultIP + ","
				resultIP = resultIP + IP
				#If we see NS in block, we know the only IP's to follow are those of NS servers....
				if " NS " in block:
				    break
			    count = 1
		    if resultIP != "":
			outputArr.append([time,realIP,queriedDomain,resultIP])

#for row in outputArr:
#    print row
outfile="/root/dns_logs/logs/dns_logs"+"_"+str(curDate)+"_"+str(curTime)
#Add some safety to deleting stuff
if "/tmp/dns.pcap" in fname:
#    shutil.move(fname,"/tmp/oldFiles/")
    os.remove(fname)
with open(outfile, "w") as out:
    writer = csv.writer(out)
    writer.writerows(outputArr)
