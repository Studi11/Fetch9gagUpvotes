# Fetch9gagUpvotes

This repo consists of 2 python scripts, getUpvoteLinks.py and downloadLinks.py.
As the names imply the first one gathers links to the media of posts you upvoted and the second
can then download those media files.

## Install
Using pipenv execute `pipenv install`, the dependencies will get downloaded

Additionally you'll have to have the correct chromedriver version installed.
The version of your Chrome Browser has to be the same and can be checked by going to
settings -> About

### Dependencies
- requests
- selenium
- beautifulsoup

## Usage getUpvoteLinks.py
First, log in to your 9gag account on the chrome webbrowser. This will store the authenticating cookie that
is necessary to get your private upvotes.

Then run `pipenv run python getUpvoteLinks.py [your9gagUsername]` inserting your own username.

An optional additional argument is the filename the links get saved into. It will be stored as a .json file.
If the file already exists, posts will get added if they are not in the file yet (media links are compared).
The default is `upvoted_posts.json`.

## Usage downloadLinks.py

Run `pipenv run python downloadLinks.py`

An optional additional argument is the filename with links to use. The default `upvoted_posts.json`.

A second argument is the relative path to the folder the results get stored into. The default is
`./download`

## Todo:

- handle youtube content
