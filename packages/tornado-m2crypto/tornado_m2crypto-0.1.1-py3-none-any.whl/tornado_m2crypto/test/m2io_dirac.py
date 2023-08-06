#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Simple HTTPS test server
# Run with: tox -e m2io_https
# Client: curl -k -v https://localhost:12345

import os
import M2Crypto
from M2Crypto import X509

#THIS WORKS AS TEST BUT NOT HERE WHY ????
CERTDIR = os.path.join(os.path.dirname(__file__), 'certs/')
SSL_OPTS = {

  'certfile': CERTDIR + 'MrBoincHost/hostcert.pem',
  'keyfile': CERTDIR + 'MrBoincHost/hostkey.pem',
  'cert_reqs': M2Crypto.SSL.verify_peer,
  'ca_certs': CERTDIR + 'ca/ca.cert.pem',
}


# Patching
from tornado_m2crypto.m2netutil import m2_wrap_socket
import tornado.netutil
tornado.netutil.ssl_wrap_socket = m2_wrap_socket

import tornado.iostream
tornado.iostream.SSLIOStream.configure('tornado_m2crypto.m2iostream.M2IOStream')

import tornado.httputil
tornado.httputil.HTTPServerRequest.configure('tornado_m2crypto.m2httputil.M2HTTPServerRequest')



import tornado.httpserver
import tornado.ioloop
import tornado.web

######### DIRAC TESTS #########################################################################################
from DIRAC.Core.Security.X509Chain import X509Chain
from DIRAC.Core.Security.X509Certificate import X509Certificate
from DIRAC.Core.Security.ProxyInfo import getProxyInfo

# To get this to work, Core/Security/__init__.py has to be modified not to register the two VOMS OID


##############################################################################################################

class getToken(tornado.web.RequestHandler):
    def get(self):
        # pemCert = self.request.connection.stream.socket.get_peer_cert().as_pem() #False =  dictionnaire, True=Binaire
        # print("CERT !!", pemCert)
        # diracCert = X509Certificate()
        # print("LOADING %s", diracCert.loadFromString(pemCert))
        # print("DIRAC CERT !!", diracCert.getSubjectDN())
        chainAsText =self.request.get_ssl_certificate().as_pem()
        print("First in the list" % chainAsText)
        diracChain = X509Chain()
        cert_chain = self.request.get_ssl_certificate_chain()
        for cert in cert_chain:
          # diracCert = X509Certificate()
          # diracCert.loadFromString(cert.as_pem())
          # diracCertList.append(diracCert)
          chainAsText += cert.as_pem()
          print("one more" % cert.get_subject())
        diracChain.loadChainFromString(chainAsText)

        from pprint import pprint
        proxyInfo = getProxyInfo(diracChain)
        if proxyInfo['OK']:
          pprint(proxyInfo['Value'])
        self.write("hello\n\n")

application = tornado.web.Application([
    (r'/', getToken),
])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application, ssl_options=SSL_OPTS)
    http_server.listen(12345)
    tornado.ioloop.IOLoop.instance().start()
