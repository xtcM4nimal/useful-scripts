#!/bin/sh
# Usage: rblcheck [IP ... ]

# FIXME: If there is a network outage, this script says "not listed" for pretty much everything

IPS="$*"
[ "$IPS" ] || IPS=$( ip addr ls | sed '/ inet \(127\.\|192\.168\.\|10\.\)/ d ; / inet / { s:.* inet :: ; s:/.*:: ; p } ; d ' )
MYIP=$( /sbin/ip route get 8.8.8.8 | sed '/src/ { s/.* src //; s/ .*//;p } ; d')

BLACKLISTS="
    cbl.abuseat.org
    spam.dnsbl.sorbs.net
"

if tty -s ; then
    RED=`tput setaf 1`
    GREEN=`tput setaf 2`
    RESET=`tput sgr0`
else
    RED=
    GREEN=
    RESET=
fi

for IP in $IPS ; do

    # Reverse digits in IP address for lookup ...
    REVERSEDIP=$(echo $IP |
      sed -ne "s~^\([0-9]\{1,3\}\)\.\([0-9]\{1,3\}\)\.\([0-9]\{1,3\}\)\.\([0-9]\{1,3\}\)$~\4.\3.\2.\1~p"
    )

    # -- do a REVERSEDIP ( address -> name) DNS lookup
    REVERSE_DNS=$(dig +short -x $IP)

    if [ "$IP" = "$MYIP" ] ; then
        PRIMARY="(Primary IP) "
    else
        PRIMARY=""
    fi
    echo "rblcheck $IP $PRIMARY# on `hostname` at $(date '+%Y-%m-%d %H:%M:%S') "

    # -- cycle through all the blacklists
    for BLACKLIST in ${BLACKLISTS} ; do

        #print the query date and time
        #show the reversed IP and append the name of the blacklist
        #printf "%-40s" " ${REVERSEDIP}.${BLACKLIST}."

        # use dig to lookup the name in the blacklist
        #echo "$(dig +short -t a ${REVERSEDIP}.${BLACKLIST}. |  tr '\n' ' ')"
        if dig +short -t a $REVERSEDIP.$BLACKLIST | grep -q ^127\. ; then
            LISTED="${RED}LISTED: $(dig +short -t txt $REVERSEDIP.$BLACKLIST )${RESET}"
        else
            LISTED="${GREEN}not listed${RESET}"
        fi
        printf "  %-16s  %-25s %s\\n" "$IP" "$BLACKLIST" "$LISTED"
    done
done