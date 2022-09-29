import time

import threading
from lib.vs_wrc201 import i2c_motor
from lib.shared_memory import Queue
from lib.PID import PID
from config.public import *
from utils.txt import write_pid

calc_wall_distance = Queue("/wallCalcQueue")
key_command = Queue("/keyQueue", False)
direction = Queue("/directionQueue")
obstacle = Queue("/obstacleQueue")

i2c_motor.init()

START = 0
DIRECTION = 'l'
POWER = 30
MIN_POWER = 0
MAX_POWER = 30
# KP = 0.95
# KI = 0.0
# KD = 9.5 

pid = PID(KP, KI ,KD, WALL_DISTANCE)


def clamp(out):
    if out < -MAX_POWER:
        out = -MAX_POWER
    if out > MAX_POWER:
        out = MAX_POWER
    return out

def queue_receiver(function):
    return function.queue.receive()[0].decode()

def queue_receiver2(function):
    try:
       if function.queue.current_messages:
           return function.queue.receive()[0].decode()
    except:
       pass
    return None

def get_command(command_list):
    global START, DIRECTION, POWER, MIN_POWER, MAX_POWER
    command = command_list.split(',')
    #print(command)
    START = int(command[START_CMD])
    DIRECTION = command[DIRECTION_CMD]
    direction.queue.send(str(DIRECTION))
    POWER = int(command[POWER_CMD])
    MIN_POWER = int(command[POWERMIN_CMD])
    MAX_POWER = int(command[POWERMAX_CMD])
    pid.setKValue(float(command[KP_CMD]), float(command[KI_CMD]), float(command[KD_CMD]))
    if int(command[WRITE]):
         write_pid(PID_FILE ,pid.Kp, pid.Ki, pid.Kd)
    

def recv_command():
    while True:
        key_command_msg = queue_receiver2(key_command)
        if key_command_msg:
            get_command(key_command_msg)
        time.sleep(0.005)

calc_wall_distance_msg = 0
def recv_wall_distance():
    global calc_wall_distance_msg
    while True:
        calc_wall_distance_msg = queue_receiver(calc_wall_distance)
        #print(calc_wall_distance_msg) 
        time.sleep(0.0001)

def recv_obstacle():
    while True:
        obstacle_msg = int(queue_receiver(obstacle))
        #print(obstacle_msg)
        if obstacle_msg:
             pid.setPoint = WALL_DISTANCE - WALL_SUBSTACTOR
        else:
             pid.setPoint = WALL_DISTANCE
        #print(pid.setPoint)

left_power = 0
right_power = 0
 
def move():
   global left_power, right_power
   if START:
      if calc_wall_distance_msg:
         #print(pid.setPoint)
         out = pid.update(int(float(calc_wall_distance_msg)))
         # print(out)

         if DIRECTION == DIRECTION_DEFAULT:
             left_power = int(POWER - out)
             right_power = int(POWER + out)

         if DIRECTION == DIRECTION_RIGHT:
             left_power = int(POWER + out)
             right_power = int(POWER - out)


         left_power = clamp(left_power)
         right_power= clamp(right_power)
         
         i2c_motor.drive_motor(-left_power, right_power)
   else:
      pid.clear()
   
def main():
    while True:
        move()       
        time.sleep(0.01)

command_receiver = threading.Thread(target=recv_command)
wall_distance_receiver = threading.Thread(target=recv_wall_distance)
obstacle_receiver = threading.Thread(target=recv_obstacle)

# start after every other threads starts
main_thread = threading.Thread(target=main)

command_receiver.start()
wall_distance_receiver.start()
obstacle_receiver.start()
main_thread.start()

command_receiver.join()
wall_distance_receiver.join()
obstacle_receiver.join()
main_thread.join()


