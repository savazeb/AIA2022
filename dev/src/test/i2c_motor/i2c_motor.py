import vs_wrc201_i2c
import time

MU8_O_EN = 0x10
MU8_TRIG = 0x11
MS16_FB_PG0 = 0x20
MS16_FB_PG1 = 0x22

MS32_A_POS0 = 0x48
MS32_A_POS1 = 0x4C

MS16_T_OUT0 = 0x50
MS16_T_OUT1 = 0x52

MU16_FB_PCH0 = 0x30
MU16_FB_PCH1 = 0x32


i2c = vs_wrc201_i2c.VsWrc201I2c(0x10)


def handle_wrc201_i2c(addr, data, length, cmd):
    if cmd == "w":
        try:
            if length == 4:  # 4byte
                i2c.write_4_byte(addr, data)
            elif length == 2:  # 2byte
                i2c.write_2_byte(addr, data)
            elif length == 1:  # 1byte
                i2c.write_1_byte(addr, data)
        except IOError as e:
            return None
    elif cmd == "s":
        try:
            i2c.send_write_map()
        except IOError as e:
            return None


def drive_motor(r_speed, l_speed):
    handle_wrc201_i2c(MS32_A_POS0, r_speed, 4, "w")
    handle_wrc201_i2c(MS32_A_POS1, l_speed, 4, "w")
    handle_wrc201_i2c(MU8_TRIG, 0x03, 1, "w")


def main():
    i2c.set_dev_addr(0x10)
    i2c.read_all()
    i2c.init_memmap(2.0)
    i2c.send_write_map()

    handle_wrc201_i2c(MU8_O_EN, 0x00, 1, "w")
    handle_wrc201_i2c(MU8_TRIG, 0x0C, 1, "w")
    handle_wrc201_i2c(MS16_FB_PG0, 0x0080, 2, "w")
    handle_wrc201_i2c(MS16_FB_PG1, 0x0080, 2, "w")
    handle_wrc201_i2c(MU16_FB_PCH0, 0x09C4, 2, "w")
    handle_wrc201_i2c(MU16_FB_PCH1, 0x09C4, 2, "w")
    handle_wrc201_i2c(MU8_O_EN, 0x03, 1, "w")

    # handle_wrc201_i2c(MU8_O_EN,0x03,1,'s')

    for x in range(500):
        drive_motor(20, -20)
        time.sleep(0.001)
    # drive_motor(0, 0)


main()
