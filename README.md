# wipy-urllib

This version of urllib is designed to be used with Micropython.

Usage is similar to normal urllib:

> import urllib
> f = urllib.urlopen('http://www.micropython.org')
> f.code
> f.headers
> f.read()

There are also methods for urlencoding:
> urllib.urlencode('abc 123')
> urllib.quote('abc 123')
> urllib.quote_plus('abc 123')
> urllib.unquote('abc%20123')
> urllib.unquote_plus('abc+123')

Discussion available at http://forum.micropython.org/viewtopic.php?f=11&t=1080
