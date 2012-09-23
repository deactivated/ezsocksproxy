from gevent import monkey
monkey.patch_all()

import cookielib
import urllib
import urllib2
import urlparse
import webob
import lxml.html
import socks

from gevent.pywsgi import WSGIServer

from .socks_handler import SocksiPyHandler


def spool(in_f):
    buf = in_f.read(512)
    if buf:
        yield buf

    while True:
        buf = in_f.read(4096)
        if buf:
            yield buf
        else:
            break


def rewrite_links(body, base_url, proxy_url):
    def make_proxy_url(link):
        return "%s?%s" % (proxy_url, urllib.urlencode({'url': link}))

    x = lxml.html.fromstring(body)
    x.make_links_absolute(base_url=base_url)
    x.rewrite_links(make_proxy_url)
    return lxml.html.tostring(x)


class EZProxy(object):

    def __init__(self, proxy_addr, socks_addr):
        self.proxy_host, self.proxy_port = proxy_addr
        self.socks_host, self.socks_port = socks_addr
        self.cookies = cookielib.CookieJar()

    def urlopen(self, url):
        socks_handler = SocksiPyHandler(socks.PROXY_TYPE_SOCKS5,
                                        self.socks_host, self.socks_port)
        cookie_handler = urllib2.HTTPCookieProcessor(self.cookies)
        opener = urllib2.build_opener(socks_handler, cookie_handler)
        request = urllib2.Request(url.encode('utf8'), headers={
            'User-Agent': '',
        })
        return opener.open(request)

    def __call__(self, environ, start_response):
        req = webob.Request(environ)

        proxy_url = "http://%s:%s/login" % (self.proxy_host, proxy_port)

        status = '200 OK'
        headers = {"Content-Type": "text/html"}
        body = []

        if req.path == "/login" and "url" in req.params:
            url = req.params["url"]
            try:
                f = self.urlopen(url)
            except urllib2.HTTPError as e:
                status = "%d %s " % (e.code, e.msg)
            except urllib2.URLError as e:
                status = "400 Bad Request"
            else:
                info = f.info()
                headers['Content-Type'] = info.get('content-type')
                if headers['Content-Type'].find('html') >= 0:
                    body = [rewrite_links(f.read(),
                                          base_url=url,
                                          proxy_url=proxy_url)]
                else:
                    body = spool(f)

        start_response(status, headers.items())
        for chunk in body:
            yield chunk


def serve(bind_addr, socks_addr):
    """
    Spawn an EZProxy on bind_addr and tunnel network access via the proxy at
    socks_addr.
    """
    app = EZProxy(bind_addr, socks_addr)
    WSGIServer(bind_addr, app).serve_forever()
