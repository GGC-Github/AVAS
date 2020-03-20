#!/bin/sh

Linux_001() {
	echo "[CODE-START | $1]" > test.txt
	echo "[DATA-START]" >> test.txt

	get_val=`ps -ef | grep -v grep | grep sshd`
	if [ "$get_val" != "" ]; then
		echo "$get_val" >> test.txt
	else
		echo "Not Found Process" >> test.txt
	fi
	echo "[DATA-END]" >> test.txt
	echo "[CODE-END]" >> test.txt
}

Linux_001 "$1"
