#!/bin/sh

echo "========== Git Auto Push Start =========="

add_file_chk=`git status | grep "nothing to commit"`
if [ "$add_file_chk" != "" ]; then
	echo "Not Found Add File"
else
	git status
	git add -A
	if [ "$1" != "" ]; then
		commit_des="$1"
	else
		commit_des=`git status | egrep -v '^[A-Z]|^$|\(' | tr -d ' \t'`
	fi
	git status
	git commit -m "$commit_des"
	git push origin master
fi

echo "==========  Git Auto Push End  =========="
