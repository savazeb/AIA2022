def write_pid(fname, kp, ki, kd):
    f = open(fname, 'w')
    f.write(f"{kp}\n{ki}\n{kd}")
    f.close()
 
