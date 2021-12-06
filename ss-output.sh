#!/bin/bash

DST=$1

touch $2

rm -f $2 

cleanup ()
{
    #echo $1 $2
	# get timestamp
	ts=$(cat $1 |   sed -e ':a; /<->$/ { N; s/<->\n//; ba; }' | grep "ESTAB"  |  grep "unacked" |  awk '{print $1}')
	echo $ts

	# get sender
	sender=$(cat $1 |   sed -e ':a; /<->$/ { N; s/<->\n//; ba; }' | grep "ESTAB"  | grep "unacked" | awk '{print $6}')
	echo $sender


	# retransmissions - current, total
	retr=$(cat $1 |   sed -e ':a; /<->$/ { N; s/<->\n//; ba; }' | grep "ESTAB"  |  grep -oP '\bunacked:.*\brcv_space'  | awk -F '[:/ ]' '{print $4","$5}' | tr -d ' ')
	echo $retr

	# get cwnd, ssthresh
	cwn=$(cat $1 |   sed -e ':a; /<->$/ { N; s/<->\n//; ba; }' | grep "ESTAB"    |  grep "unacked" | grep -oP '\bcwnd:.*(\s|$)\bbytes_acked' | awk -F '[: ]' '{print $2","$4}')
	echo $cwn

	# concatenate into one CSV
	paste -d ',' <(printf %s "$ts") <(printf %s "$sender") <(printf %s "$retr") <(printf %s "$cwn") > $2

	exit 0
}

trap "cleanup $2 $3" SIGINT SIGTERM

while [ 1 ]; do 
	ss --no-header -ein dst $DST | ts '%.s' | tee -a $2 
done

