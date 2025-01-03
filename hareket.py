# hareket işe yaramazsa bu kullanılacak
# test edilip açı hesapları yapılacak işe yararsa açı paketi import edilecek
from pymavlink import mavutil
import time

# MAVLink bağlantısı oluşturma
master = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)


# sağ ve sol dönüşlerde gerekli hesaplar yapılacak ona göre değerler verilecek
def sola_don(sol_guc, sag_guc, t):
    send_rc_channels_override(sol_guc, sag_guc)
    uyu(t)


def saga_don(sol_guc, sag_guc, t):
    send_rc_channels_override(sol_guc, sag_guc)
    uyu(t)


def zigzag1(sol_guc, sag_guc, t1, t2):
    sola_don(sol_guc, 1500, t1)
    saga_don(1500, sag_guc, t2)


def zigzag2(sol_guc, sag_guc, t1, t2):
    saga_don(1500, sag_guc, t1)
    sola_don(sol_guc, 1500, t2)


# RC_CHANNELS_OVERRIDE mesajını gönderme fonksiyonu
def send_rc_channels_override(left_speed, right_speed):
    master.mav.rc_channels_override_send(
        master.target_system,  # Hedef sistem
        master.target_component,  # Hedef bileşen
        0,  # Gaz kanalı
        0,  # Roll kanalı
        0,  # Pitch kanalı
        0,  # Yaw kanalı
        left_speed,  # Sol motor hızı (sola dönüş için)
        right_speed,  # Sağ motor hızı
        0, 0, 0, 0, 0, 0, 0)  # Diğer kanallar (kullanılmıyor)


# Sol dönüş komutunu gönderme
# send_rc_channels_override(1300, 1500)

# Belirli bir süre sonra komutu iptal etme
def uyu(t):
    time.sleep(t)


# Motor hızlarını sıfırlama (araç sabit durumda)
send_rc_channels_override(1500, 1500)
