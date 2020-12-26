#!/bin/sh

if [ "$#" -ne 1 ]; then
	echo "give your 9gag username as the first argument"
	exit 1
fi

username=$1
echo "using $username as username"

pipenv run python getUpvoteLinks.py $username
if [ "$?" -ne 0 ]; then
	pipenv install
	pipenv uninstall chromedriver-binary-auto
	pipenv install chromedriver-binary-auto
	pipenv run python getUpvoteLinks.py $username
fi
pipenv run python downloadLinks.py

