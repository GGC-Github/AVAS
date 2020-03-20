#!/bin/sh

if [ "$1" = "" ]; then
	echo ""
	echo "The parameter value is empty. Write your commit message!"
	echo "Usage: ./AutoGit.sh [ \"Commit message\" ]"
	echo ""
	exit
else
	commit_des="$1"
fi

echo "========== Git Auto Push Start =========="

add_file_chk=`git status | grep "nothing to commit"`
if [ "$add_file_chk" != "" ]; then
	echo "Not Found Add File"
else
	git status
	git add -A
	git status
	git commit -m "$commit_des"
	git push origin master
fi

echo "==========  Git Auto Push End  =========="
