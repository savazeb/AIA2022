# 2022 AIA Robotics Competition
This repository is used to store the codes for 2022 AIA robotics competition. We're using [lightrover](https://www.vstone.co.jp/products/lightrover/) and it's API as a base and controller. The robot itself has one lidar sensor on the top of it. We're utilizing its sensor to calculate the distance of the surrounding wall and follow it.

As a result, we took second place in this competition with 29 seconds. The result can be seen here. 
[2022 AIA ROBOTICS COMPETITION RESULT](http://www.aia.or.jp/contest.html)  

## Project Tree
This repository has one main directory to store the main code (./[dev](./dev/)). And a bunch of sample program for lightrover taken from its [original repository](https://github.com/vstoneofficial/lightrover_ros/tree/9bba9e5bcd71030870a1694ec858be4ec13eb90e) (./[sample](./sample/)).
```
├── dev
│   └── src
│       └── main.py
└── sample
    └── main.py
```


## Usage
The usage of this project is rather simple but some dependencies must be installed first in order to use it.

First, tmux must be installed. Use bellow command for linux distribution.
```
sudo apt update && apt install tmux -y
```

After tmux is installed you can go to [./dev/src](./dev/src/) and start `./run.sh` to run all the script.

If you want to run the script without `./run.sh`, make sure to run the script in this order to avoid blocked process caused by the fullness of query storage.
1. `./keylogger.sh`
2. `./motor.sh`
3. `./wall_calc.sh`
4. `./lidar.sh`

All the main code is stored in the [./dev/src/services](./dev/src/services/) directory. The code might be unpleasant to read because this project was rushed. Cheers!!

## LICENSE
[MIT](./LICENSE)