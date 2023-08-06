# README #

A simplest html parsing library.


Key features:

 * no third-party dependencies
 * no need to know CSS, Xpath or complicated rules to find element
 * interaction with native python lambda syntax or function-predicate
 * opportunity to work with damaged html
 * ability to use element relations (find ancestor, descendant, siblings)
 * standard find first element or find all by current filter

### Installation ###

Via pip:

`pip install py_parse`

### First example ###
Lets get src attribute (link) of the Google logo on google.com
```python
import requests
from py_parse import parse

# get content of the google web page
content = requests.get('https://www.google.com/').text
# find first element with img-tag and 'alt' attribute equal to Google (logo)
google_logo = parse(content).find(lambda e: e.tag == 'img' and e.alt == 'Google')
# prints src attribute of the logo element
print(google_logo.src)
```
You will see following result
```text
/images/branding/googlelogo/1x/googlelogo_white_background_color_272x92dp.png
```
If there is no element with current filter, you will get exception with filters text (if lamda was used)^
For code above lets say we use wrong filter
```python
google_logo = parse(content).find(lambda e: e.tag == 'img' and e.alt == 'Wrong')
```
You will see following result
```text
...traceback...
py_parse.exceptions.NoSuchElementError: No elements with current filter (e.tag == 'img' and e.alt == 'Wrong')
```
TODO - child, ancestor, sibling, descendant, mailformed html, check tags, autoclose

### Contact me ###
Lexman2@yandex.ru
