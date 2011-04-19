#!/usr/bin/python
from sys import argv
import socket
import struct
import md5

if len(argv) == 4:
  d = argv[3]
  t = ""
elif len(argv) == 5:
  d = argv[4]
  t = argv[3]
else:
  print "%s: Three or four arguments required." % (argv[0])
  exit(1)

ip = argv[1]
pwd = argv[2]

s = socket.socket(socket.AF_INET,
    socket.SOCK_DGRAM)

data = '\x01\x01\x00\x00' # ver 1, packet type notify, no flags

data += struct.pack("!4H",
    0,      # notification length
    len(t), # title length
    len(d), # description length
    len(argv[0])) # app name length
data += t + d + argv[0]
checksum = md5.new()
checksum.update(data)
checksum.update(pwd)

s.sendto(data + checksum.digest(), (ip, 9887))
