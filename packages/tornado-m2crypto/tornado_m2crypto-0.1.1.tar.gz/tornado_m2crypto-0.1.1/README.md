# tornado_m2crypto

This extension is meant to run tornado with M2Crypto instead of the standard python SSL

# Dependencies

Of course, you need M2Crypto
You need a patched version of Tornado: git+https://github.com/DIRACGrid/tornado.git@iostreamConfigurable


# How to use


The tornado_m2crypto/tests directory contains several examples.
Basically, just take any normal https server with tornado you want, and add the following at the beginning


```
# Patching
# needed because some direct calls to ssl_wrap_socket in TCPServer
from tornado_m2crypto.m2netutil import m2_wrap_socket
import tornado.netutil
tornado.netutil.ssl_wrap_socket = m2_wrap_socket


# Dynamically configurable
import tornado.iostream
tornado.iostream.SSLIOStream.configure('tornado_m2crypto.m2iostream.M2IOStream')


import tornado.httputil
tornado.httputil.HTTPServerRequest.configure('tornado_m2crypto.m2httputil.M2HTTPServerRequest')

```





# How to test

There are several types of tests.

## Unit test

Almost a copy paste of the SSLIOStream tests from tornado:

`tox -r`

## HTTPS test

A simple HTTPS server

`tox -r -e m2io_https`

You can then talk to you using (only requires `requests` package)

`python test_client.py`


## DIRAC test

An HTTPS server converting the certificate to "DIRAC certificates"

`tox -r -e m2io_dirac`

You can talk to it the same way as the normal HTTPS test, and you can give it a proxy
