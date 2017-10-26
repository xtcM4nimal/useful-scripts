# DNS server response logging
---
This is meant to live on a DNS server.
It will dump CSV logs to /root/dns_logs/logs containing what IP address queried the server, asking for what domain and tho what we resolved it.

  * Add the files to /root/dns_logs/
  * Add the cron entries

Low on memory, safe to leave on.
Uses the graceful kill on the tcpdump command to neatly create it's log file

