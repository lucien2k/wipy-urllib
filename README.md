# wipy-urllib

This version of urllib is designed to be used with Micropython.

Usage is similar to normal urllib:

> import urllib  
> f = urllib.urlopen('http://www.micropython.org')  
> f.code  
> f.headers  
> f.read()

It is possible to do posts:
> f = urllib.urlopen('http://www.someurl.com', {'input': 'value'})

There are also methods for urlencoding:
> urllib.urlencode('abc 123')  
> urllib.quote('abc 123')  
> urllib.quote_plus('abc 123')  
> urllib.unquote('abc%20123')  
> urllib.unquote_plus('abc+123')

Discussion available at http://forum.micropython.org/viewtopic.php?f=11&t=1080

# urequests

First version of urequests for micropython

Supports:
 - SSL
 - Cookies
 - Basic Auth
 - Custom HTTP Headers
 - GET, POST, PUT, DELETE, OPTIONS, HEAD

Similar interface to http://docs.python-requests.org/en/latest/
