#!/usr/bin/env python2
import md5
import struct

def make_checksum(data, password):
    checksum = md5.new()
    checksum.update(data)
    checksum.update(password)
    return checksum.digest()

def make_packet(appname, password, title, text):
    data = '\x01\x01\x00\x00' # ver 1, packet type notify, no flags

    data += struct.pack("!4H",
            0,              # notification length
            len(title),     # title length
            len(text),      # description length
            len(appname)    # app name length
    )
    data += title + text + appname

    return data + make_checksum(data, password)

def send_packet(data, address):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(data, (address, 9887))

# args: 
#   address, password, notification text
# or:
#   address, password, notification title, notification text
if __name__ == '__main__':
    import sys
    args = sys.argv[1:]

    address = args.pop(0)
    password = args.pop(0)

    if len(args) == 2:
        text, title = args[1], args[0]
    elif len(args) == 1:
        text, title = args[0], ""
    else:
        print "%s: Three or four arguments required." % (sys.argv[0])
        exit(1)

    packet = make_packet("cmdline notifier", password, title, text)
    send_packet(packet, address) 
