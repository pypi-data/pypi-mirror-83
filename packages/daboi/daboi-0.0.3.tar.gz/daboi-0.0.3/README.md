# Daboi Package

This is an instagram automation with selenium. 

## Prerequisities

* selenium
* chromedriver

## Features

* Likes - home feed and hashtags
* Follows - hashtags
* Unfollows
* Watch stories

## Install


```python
pip3 install daboi
```

## Run


```python
from daboi import instabot

config = {
	"user":"username",
	"password":"password",

}
instabot.Client(config)

#enjoy the stonks
```

