from pymavlink import mavutil
import time

master = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)


# iki fonksiyon da arm ve disarm ediyor 0 olunca disarm ediyor deneyip görmek lazım
def arm_et(arm):
   
    if arm == 1:
        master.arducopter_arm()
        print("Arming...")
    elif arm == 0:
        master.arducopter_disarm()
        print("Disarming...")
    else:
        print("Geçersiz parametre! 1 veya 0 olmalı.")


arm_et()


def armanddisarm(i):
    master.mav.command_long_send(master.target_system, master.target_component,
                                 mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                                 0,
                                 i, 0, 0, 0, 0, 0, 0)
    if i == 0:
        master.motors_disarmed_wait()
        print("Disarm")
    else:
        master.motors_armed_wait()
        print("Arm")


# fonksiyon çağrılıyor 0=disarm
armanddisarm()
