#!/usr/bin/env python2
# vim:et:sts=4 sw=4

from twisted.internet import protocol
import growl

GROWL_UDP_PORT=9887

class WrongCallbackException(Exception):
    pass

class GrowlProtocol(protocol.DatagramProtocol):
    def __init__(self, callback, password = None):
        if not callback or not callable(callback):
            raise WrongCallbackException()
        self.callback = callback
        self.password = password

    def datagramReceived(self, data, (host, port)):
        if len(data) < 28:
            raise growl.ProtocolException()

        if data[0] != growl.GROWL_PROTOCOL_1:
            raise growl.ProtocolException()

        if data[1] == growl.GROWL_TYPE_NOTIFY:
            p = growl.IncomingNotifyPacket(data, self.password)
            self.callback(*p.decode())

if __name__ == "__main__":
    from sys import platform

    try:
        notifier = __import__("system." + platform, globals(), locals(), ["notify"])
    except ImportError:
        print "Unsupported system platform: " + platform
        exit(1)

    from twisted.internet import reactor
    from sys import argv

    reactor.listenUDP(GROWL_UDP_PORT, GrowlProtocol(notifier.notify, "dupa.8" if len(argv) == 1 else argv[1]))
    reactor.run()
