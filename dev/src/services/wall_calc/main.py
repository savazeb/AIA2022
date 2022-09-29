from threading import Thread, Event
import posix_ipc as ipc
import numpy as np
import sys
import time
import json
import math

from lib.PID import PID
from lib.shared_memory import Queue
from utils.array import find_nearest
from config.public import *

class Direction(Queue):
   def __init__(self, qname, block=True):
        super().__init__(qname, block)
        self.data = self.reset_data()
   def set_data(self):
        while True:
            self.data = str(self.queue.receive()[0].decode())
   def reset_data(self):
        return DIRECTION_DEFAULT

direction = Direction("/directionQueue")

class Lidar(Queue):
    def __init__(self, qname, block = True):
        super().__init__(qname, block)
        self.data = self.reset_data()
        self.direction = DIRECTION_DEFAULT

    def set_data(self):
        while True:
            angles = []
            ranges = []
            lidar = self.queue.receive()
            point = eval(lidar[0].decode())
            for key in point:
                angles.append(int(key))
                ranges.append(float(point[key]))

            angles = np.array(angles)
            ranges = np.array(ranges)

            # print(angles, ranges)

            ranges_temp = []
            angles_temp = []
            if self.direction == DIRECTION_DEFAULT:
                for angle in range(360):
                    x = (540 - angle) % 360
                    idx_logic = np.argwhere(angles==x)
                    if idx_logic.size > 0:
                        angles_temp.append(angle)
                        ranges_temp.append(ranges[idx_logic][0][0])
                self.data = np.array([angles_temp, ranges_temp])
            
            if self.direction == DIRECTION_RIGHT:        
                self.data = np.array([angles, ranges])


    def reset_data(self):
        return None


lidar = Lidar("/pointQueue")

class Obstacle(Queue):
    def __init__(self, qname, block = True):
        super().__init__(qname, block)
        self.obs = 0
        self.obstacle = 0
    def scan(self):
        try:
            self.angles, self.ranges = lidar.data
            indicies = np.argwhere((self.angles < FACE_ANGLE + SCAN_RANGE_RIGHT) & (self.angles > FACE_ANGLE - SCAN_RANGE_LEFT))
            ranges = self.ranges[indicies]
            ranges = ranges[~np.all(ranges <= 0, axis = 1)]
            self.obs = np.min(ranges)
            # print(self.obs)
            if self.obs < OBSTACLE_LIMIT:
                self.obstacle = 1
                #self.queue.send(str(self.obstacle))
            else:
                self.obstacle = 0
            self.queue.send(str(self.obstacle))
        except:
            pass

obstacle = Obstacle("/obstacleQueue")

class sensor_thread(Thread):
    def __init__(self, name, delay, *args, **kwargs):
        super(sensor_thread, self).__init__(*args, **kwargs)
        self._stopper = Event()
        self.name = name
        self.delay = delay
    def stopit(self):
        self._stopper.set()
    def stopped(self):
        return self._stopper.isSet()
    def run(self):
        while True:
            if self.stopped():
                return
            if self.name == 'direction':
                direction.set_data()
            if self.name == 'lidar':
                lidar.set_data()
            if self.name == 'obstacle':
                obstacle.scan()
            time.sleep(self.delay)



def main():
    calc_wall_distance = Queue("/wallCalcQueue")

    SENSOR_TYPE = [('direction', 0.0), ('lidar', 0.0), ('obstacle', 0.001)]
    workers = []

    for name, delay in SENSOR_TYPE:
        print('[info] start thread : ' , name)
        thread = sensor_thread(name, delay)
        workers.append(thread)
        thread.start()

    while True:
        lidar.direction = direction.data
        #print(obstacle.obs, obstacle.obstacle)
        #print(lidar.direction)
        if type(lidar.data) == np.ndarray:
            angles, ranges = lidar.data
            right_hand = float(ranges[find_nearest(angles, HAND_ANGLE)])
            helper_hand = float(ranges[find_nearest(angles, HELPER_HAND_ANGLE)])
            # print(right_hand, helper_hand)
            teta = math.radians(DELTA_ANGLE)
            if right_hand > 0 and helper_hand > 0:
                alpha = math.atan((right_hand * math.cos(teta) - helper_hand) / (right_hand * math.sin(teta)))
                alpha = math.degrees(alpha)
                rx_distance = helper_hand * math.cos(math.radians(alpha)) 
                calc_wall_distance.queue.send(str(rx_distance))
                #print(right_hand, helper_hand, rx_distance)
            time.sleep(0.01)
            # print(len(angles))
            # for idx, angle in enumerate(angles):
            #     # if idx > 24000:
            #      print(angle, ranges[idx])
            #     time.sleep(0.01)

        #lidar.data = lidar.reset_data()

if __name__ == "__main__":
    main()
