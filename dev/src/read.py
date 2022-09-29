import posix_ipc as ipc
import time
import struct
# import numpy as np
# import json

point_q = ipc.MessageQueue("/keyQueue", ipc.O_CREAT)


while True:
    angles = []
    ranges = []
    msg = point_q.receive()
    data = msg[0].decode('utf-8')
    print(data)