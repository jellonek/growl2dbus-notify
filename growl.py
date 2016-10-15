# vim:et:sts=4 sw=4
#
# Growl decoding routines
#

import logging
import md5
import struct

GROWL_TYPE_NOTIFY = '\x01'
GROWL_TYPE_REGISTER = '\x00'
GROWL_PROTOCOL_1 = '\x01'
GROWL_PROTOCOL_AES128 = '\x02'

logger = logging.getLogger(__name__)

class DecoderException(Exception):
    pass

class ProtocolException(DecoderException):
    pass

class DataLenException(DecoderException):
    pass

class ChecksumException(DecoderException):
    pass

class IncomingPacket(object):
    """Common growl packet decoding methods"""

    def __init__(self, data, password = None):
        """Check packet validity"""
        self._verify_existence_of_data(data)
        self.data = data

        self._verify_protocol()
        self._verify_checksum(password, data)

    def get_protocol(self):
        return self.data[0]

    def get_type(self):
        if self.data:
            return self.data[1]

    @staticmethod
    def _verify_existence_of_data(data):
        if data == None or len(data) == 0:
            raise DataLenException()

    def _verify_protocol(self):
        if self.data[0] != GROWL_PROTOCOL_1:
            # TODO: other than plain text protocol (ex. AES) unsupported
            raise ProtocolException()

    def _verify_checksum(self, password, data):
        checksum = md5.new()
        checksum.update(self.data[:-16])

        if password:
            checksum.update(password)

        if data[-16:] != checksum.digest():
            logger.debug("data: %s" % repr(data[-16:]))
            logger.debug("digest: %s" % checksum.digest())
            raise ChecksumException()
        

class IncomingNotifyPacket(IncomingPacket):
    def __init__(self, data, password = None):
        IncomingPacket.__init__(self, data, password)
        if data[1] != GROWL_TYPE_NOTIFY:
            raise ProtocolException()

    def decode(self):
        self.flags, nlen, tlen, dlen, alen = struct.unpack("!5H", self.data[2:12])
        self.notification, self.title, self.description, self.application = \
            struct.unpack(
                "%ds%ds%ds%ds" % (nlen, tlen, dlen, alen),
                self.data[12:12+nlen+tlen+dlen+alen]
            )
        return self.notification, self.title, self.description, self.application
