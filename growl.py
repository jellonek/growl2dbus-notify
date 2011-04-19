#!/usr/bin/env python

# Growl decoding routines

import md5
import struct

GROWL_TYPE_NOTIFY = '\x01'
GROWL_TYPE_REGISTER = '\x00'
GROWL_PROTOCOL_1 = '\x01'
GROWL_PROTOCOL_AES128 = '\x02'

class GrowlPacketProtocolException(Exception):
  pass

class GrowlPacketDataLenException(Exception):
  pass

class GrowlPacketChecksumException(Exception):
  pass

class GrowlInputPacket(object):
  """Common growl packet decoding"""

  def __init__(self, data, password = None):
    """Check packet validity"""
    if data == None or len(data) == 0:
      raise GrowlPacketDataLenException()

    self.data = data

    if data[0] != GROWL_PROTOCOL_1:
      # fixme: other than plain text protocol (ex. AES) unsupported
      raise GrowlPacketProtocolException()

    checksum = md5.new()
    checksum.update(self.data[:-16])
    if password:
      checksum.update(password)
    if data[-16:] != checksum.digest():
      print repr(data[-16:])
      print repr(checksum.digest())
      raise GrowlPacketChecksumException()

  def getProtocol(self):
    if self.data:
      return self.data[0]

  def getType(self):
    if self.data:
      return self.data[1]

class GrowlInputNotifyPacket(GrowlInputPacket):
  def __init__(self, data, password = None):
    GrowlInputPacket.__init__(self, data, password)
    if data[1] != GROWL_TYPE_NOTIFY:
      raise GrowlPacketProtocolException()

  def decode(self):
    (self.flags, nlen, tlen, dlen, alen) = struct.unpack("!5H", self.data[2:12])
    (self.notification, self.title, self.description, self.application) = \
	struct.unpack("%ds%ds%ds%ds" % (nlen, tlen, dlen, alen), self.data[12:12+nlen+tlen+dlen+alen])
    return self.notification, self.title, self.description, self.application

# vim:et:sts=2 sw=2
