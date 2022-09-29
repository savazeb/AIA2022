import posix_ipc as ipc
import time
import struct
import numpy as np
import json

point_q = ipc.MessageQueue("/pointQueue", ipc.O_CREAT)

while True:
    st = time.time()
    angles = []
    ranges = []
    lidar = point_q.receive()
    point = eval(lidar[0].decode())

    for key in point:
        angles.append(int(key))
        ranges.append(float(point[key]))
        # print("{} : {}".format(key, data[key]))
    angles = np.array(angles)
    ranges = np.array(ranges)
    print(ranges)
    print(time.time() - st)
