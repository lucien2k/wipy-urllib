"""Open an arbitrary URL.

Adapted for Micropython by Alex Cowan <acowan@gmail.com>

Includes some elements from the original urllib and urlencode libraries for Python
"""

import socket
try:
    import ussl as ssl
except:
    import ssl

class URLOpener:
    def __init__(self, url, post_data={}):
        self.code = 0
        self.headers = {}
        self.body = ""
        self.url = url
        [scheme, host, path, data] = urlparse(self.url)
        if scheme == 'http':
            addr = socket.getaddrinfo(host, 80)[0][-1]
            s = socket.socket()
            s.settimeout(5)
            s.connect(addr)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SEC)
            sock.settimeout(5)
            s = ssl.wrap_socket(sock)
            s.connect(socket.getaddrinfo(host, 443)[0][4])
        if post_data:
            data = urlencode(post_data)
            #print('POST %s HTTP/1.0\r\nHost: %s\r\n\r\n%s\r\n' % (path or '/', host, data.strip()))
            s.send(b'POST %s HTTP/1.0\r\nHost: %s\r\n\r\n%s\r\n' % (path or '/', host, data.strip()))
        else:
            #print('GET %s%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path or '/', '?'+data.strip(), host))
            s.send(b'GET %s%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path or '/', '?'+data.strip(), host))
        while 1:
            recv = s.recv(1024)
            if len(recv) == 0: break
            self.body += recv.decode()
        s.close()
        self._parse_result()

    def read(self):
        return self.body

    def _parse_result(self):
        self.body = self.body.split('\r\n')
        while self.body:
            line = self.body.pop(0).strip()
            if line == '':
                 break
            if line[0:4] == 'HTTP':
                data = line.split(' ')
                self.code = int(data[1])
                continue
            if len(line.split(':')) >= 2:
                data = line.split(':')
                self.headers[data[0]] = (':'.join(data[1:])).strip()
                continue
        self.body = '\r\n'.join(self.body)
    	return

def urlparse(url):
    scheme = url.split('://')[0].lower()
    url = url.split('://')[1]
    host = url.split('/')[0]
    path = '/'
    data = ""
    if host != url:
        path = ''.join(url.split('/')[1:])
        if path.count('?'):
            if path.count('?') > 1:
                raise Exception('URL malformed, too many ?')
            [path, data] = path.split('?')
    return [scheme, host, path, data]

def urlopen(url, post_data={}):
    orig_url = url
    attempts = 0
    result = URLOpener(url, post_data)
    ## Maximum of 4 redirects
    while attempts < 4:
        attempts += 1
        if result.code in (301, 302):
            url = result.headers.get('Location', '')
            if not url.count('://'):
                [scheme, host, path, data] = urlparse(orig_url)
                url = '%s://%s%s' % (scheme, host, url)
            if url:
                result = URLOpener(url)
            else:
                raise Exception('URL returned a redirect but one was not found')
        else:
            return result
    return result

always_safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'abcdefghijklmnopqrstuvwxyz'
               '0123456789' '_.-')

def quote(s, safe = '/'):
    res = []
    replacements = {}
    for c in s:
        if c in always_safe:
            res.append(c)
            continue
        res.append('%%%x' % ord(c))
    return ''.join(res)

def quote_plus(s, safe = ''):
    if ' ' in s:
        s = quote(s, safe + ' ')
        return s.replace(' ', '+')
    return quote(s, safe)

def unquote(s):
    """Kindly rewritten by Damien from Micropython"""
    """No longer uses caching because of memory limitations"""
    res = s.split('%')
    for i in xrange(1, len(res)):
        item = res[i]
        try:
            res[i] = chr(int(item[:2], 16)) + item[2:]
        except ValueError:
            res[i] = '%' + item
    return "".join(res)

def unquote_plus(s):
    """unquote('%7e/abc+def') -> '~/abc def'"""
    s = s.replace('+', ' ')
    return unquote(s)

def urlencode(query):
    if isinstance(query, dict):
        query = query.items()
    l = []
    for k, v in query:
        k = quote_plus(str(k))
        v = quote_plus(str(v))
        l.append(k + '=' + v)
    return '&'.join(l)

