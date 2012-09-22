"""
SocksiPy handler for urllib2

version: 0.2

author: e<e@tr0ll.in>

This module provides a urllib2 Handler which you can use to tunnel connections
through a SOCKS proxy without monkey patching socket and httplib.
"""

import urllib2
import httplib
import socks


class SocksiPyConnection(httplib.HTTPConnection):

    def __init__(self, proxy_type, proxy_addr, proxy_port=None,
                 rdns=True, username=None, password=None, *args, **kwargs):
        self.proxy_args = (proxy_type, proxy_addr, proxy_port,
                           rdns, username, password)
        httplib.HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(*self.proxy_args)
        if isinstance(self.timeout, (int, long, float)):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))


class SocksiPyHandler(urllib2.HTTPHandler):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        urllib2.HTTPHandler.__init__(self)

    def http_open(self, req):
        def build(host, port=None, strict=None, timeout=0):
            return SocksiPyConnection(*self.args,
                                      host=host, port=port,
                                      strict=strict, timeout=timeout,
                                      **self.kwargs)

        return self.do_open(build, req)
