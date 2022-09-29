tmux new-session -d -s run-session "./keylogger.sh"

tmux split-window -h 
tmux split-window -h "./lidar.sh"
tmux select-pane -t 0
tmux select-layout even-horizontal
tmux split-window -v "./wall_calc.sh"
tmux select-pane -t 3
tmux split-window -v "./motor.sh"

tmux a -t run-session
