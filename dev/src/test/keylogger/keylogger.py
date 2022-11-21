import posix_ipc as ipc
import time
import struct


point_q = ipc.MessageQueue("/keyQueue", ipc.O_CREAT)


while True:
    msg = point_q.receive()
    data = msg[0].decode('utf-8')
    print(data)
