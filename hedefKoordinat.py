from pymavlink import mavutil
import time

# MAVLink bağlantısını kurma
master = mavutil.mavlink_connection('tcp:127.0.0.1:5760')
master.wait_heartbeat()


# Aracı GUIDED moda geçirme fonksiyonu
def set_mode(master, mode):
    if mode not in master.mode_mapping():
        print("Mode '{}' not found".format(mode))
        print('Supported modes:', list(master.mode_mapping().keys()))
        return

    mode_id = master.mode_mapping()[mode]
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)

    while True:
        ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True)
        if ack_msg.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
            print("Mode set to %s" % mode)
            break


# Aracı GUIDED moda geçirme
set_mode(master, 'GUIDED')


# Hedef koordinatlara gitme fonksiyonu
def goto_position_target_global_int(master, lat, lon, alt):
    master.mav.set_position_target_global_int_send(
        0,
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        0b0000111111111000,  # Mask (ignores velocity, acceleration and yaw)
        int(lat * 1e7), int(lon * 1e7), alt,
        0, 0, 0,
        0, 0, 0,
        0, 0)

# Hedef koordinatlarını dinleme ve alma
def get_target_coordinates(master):
    while True:
        # recv_match -> Bu fonksiyon, belirli türdeki MAVLink mesajlarını dinler. Burada MISSION_ITEM ve MISSION_CURRENT mesajlarını dinlenir
        # MISSION_ITEM: Bu mesaj, Mission Planner'dan gönderilen görev öğelerinin koordinatlarını içerir
        # MISSION_CURRENT: Bu mesaj, mevcut görev öğesinin indeksini gösterir. Bu mesaj, genellikle aracın hangi görev öğesinde olduğunu belirtir
        msg = master.recv_match(type=['MISSION_ITEM', 'MISSION_CURRENT'], blocking=True)
        if msg is not None:
            if msg.get_type() == 'MISSION_ITEM':
                lat = msg.x  # enlem
                lon = msg.y  # boylam
                alt = msg.z  # irtifa
                print("Received Target Coordinates: Lat=%.6f, Lon=%.6f, Alt=%.2f" % (lat, lon, alt))
                return lat, lon, alt
            elif msg.get_type() == 'MISSION_CURRENT':
                print("Mission current index: %d" % msg.seq)
        time.sleep(1)


# Hedef koordinatlarını al ve git
lat, lon, alt = get_target_coordinates(master)
goto_position_target_global_int(master, lat, lon, alt)