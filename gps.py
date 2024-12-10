from pymavlink import mavutil

def gps_verileri_oku():
    # Uçuş kontrol cihazına bağlan
    master = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)

    # GLOBAL_POSITION_INT mesajlarını talep et
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        0,
        mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT,
        0, 0, 0, 0, 0, 0
    )

    # GPS verilerini almak için bir döngü başlat
    
        # Mavlink mesajlarını al
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)

        # GPS verilerini al
    if msg:
            lat = msg.lat / 1e7
            lon = msg.lon / 1e7
            alt = msg.alt / 1e3

    return lat, lon, alt

if __name__ == "__main__":
    gps_verileri_oku()
