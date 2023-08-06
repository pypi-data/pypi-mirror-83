# url_regex
Regular expression for matching URLs in Python. This project was made with inspirations from [url-regex for NodeJS](https://github.com/kevva/url-regex), I wanted something similar to Python, so here we are.

## Requirements
- Python 3.6 or above

## Install
pip install url_regex

## Example
```py
import url_regex
findlinks = url_regex.UrlRegex("Hi guys, check out my SoundCloud 🔥: https://soundcloud.com/invalidLink420")

findlinks.detect  # True
findlinks.links  # [<Url full=https://soundcloud.com/invalidLink420 domain=soundcloud.com protocol=https://]
```
