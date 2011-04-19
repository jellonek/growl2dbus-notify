#!/usr/bin/env python

from twisted.internet.protocol import DatagramProtocol
import growl

GROWL_UDP_PORT=9887

class GrowlWrongCallbackException(Exception):
  pass

class GrowlProtocol(DatagramProtocol):
  def __init__(self, callback, password = None):
    if not callback or not callable(callback):
      raise GrowlWrongCallbackException()
    self.callback = callback
    self.password = password

  def datagramReceived(self, data, (host, port)):
    if len(data) < 28:
      raise growl.GrowlPacketProtocolException()

    if data[0] != growl.GROWL_PROTOCOL_1:
      raise growl.GrowlPacketProtocolException()

    if data[1] == growl.GROWL_TYPE_NOTIFY:
      p = growl.GrowlInputNotifyPacket(data, self.password)
      self.callback(*p.decode())

if __name__ == "__main__":
  import dbus

  def dbus_notify(notification, title, description, application):
    notify_object = dbus.SessionBus().get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    notify_interface = dbus.Interface(notify_object, 'org.freedesktop.Notifications')
    notify_interface.Notify(application, 0, "", title, description, {}, {}, 8000)

  from twisted.internet import epollreactor
  epollreactor.install()

  from twisted.internet import reactor
  from sys import argv

  reactor.listenUDP(GROWL_UDP_PORT, GrowlProtocol(dbus_notify, "dupa.8" if len(argv) == 1 else argv[1]))
  reactor.run()

# vim:et:sts=2 sw=2
