#gyro olmazsa bu denenecek
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import time

# MPU9255 sensörünü başlatın
mpu = MPU9250(
    address_ak=AK8963_ADDRESS,  # Gyro'nun adresi
    address_mpu=MPU9250_ADDRESS_68,  # MPU'nun adresi
    bus=1,  # I2C bus numarası
    gfs=GFS_250,  # Gyro tam ölçek aralığı (±250 dps)
    afs=AFS_2G,  # İvmeölçer tam ölçek aralığı (±2G)
    mfs=AK8963_BIT_16,  # Manyetometre tam ölçek aralığı (16 bit)
    mode=AK8963_MODE_C100HZ)  # Manyetometre çalışma modu (100Hz)

mpu.calibrate()  # Sensörü kalibre edin
mpu.configure()  # Sensörü yapılandırın

# Fonksiyon ile sadece gyrodan veri okuyun
def read_gyro_data():
    gyro_data = mpu.readGyroscopeMaster()
    gyro_x = gyro_data[0]
    gyro_y = gyro_data[1]
    gyro_z = gyro_data[2]
    return gyro_x, gyro_y, gyro_z

try:
    while True:
        gyro_x, gyro_y, gyro_z = read_gyro_data()
        print(f"Gyro X: {gyro_x}, Gyro Y: {gyro_y}, Gyro Z: {gyro_z}")
        time.sleep(0.1)  # 0.1 saniye bekleme

except KeyboardInterrupt:
    print("Program sonlandırıldı.")