WALL_DISTANCE = 75
WALL_SUBSTACTOR = 15
# WALL_DISTANCE = 20

KP = 0.95
KI = 0
KD = 9.5

MAX_POWER = 30
MIN_POWER = 0
DEFAULT = 30

DELTA_ANGLE = 65
HAND_ANGLE = 180
HELPER_HAND_ANGLE = HAND_ANGLE + DELTA_ANGLE
FACE_ANGLE = 270
SCAN_RANGE_RIGHT = 40
SCAN_RANGE_LEFT = 90
OBSTACLE_LIMIT = 50
WALL_THRES = 1
WALL_LEFT_BOUND = WALL_DISTANCE - WALL_THRES
WALL_RIGHT_BOUND = WALL_DISTANCE + WALL_THRES

DIRECTION_DEFAULT = 'l'
DIRECTION_RIGHT = 'r'

# message loc from keylogger
START_CMD = 0
DIRECTION_CMD = 1
POWER_CMD = 2
POWERMIN_CMD = 3
POWERMAX_CMD = 4
KP_CMD = 5
KI_CMD = 6
KD_CMD = 7
WRITE = 8

PID_FILE = "pid.conf"