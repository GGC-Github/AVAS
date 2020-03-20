#!/bin/sh

commit_des="$1"
echo "$commit_des"
echo "========== Git Auto Push Start =========="

git status
git add -A
git status
git commit -m "$commit_des"
git push origin master

echo "==========  Git Auto Push End  =========="
