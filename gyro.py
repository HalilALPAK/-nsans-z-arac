import mpu6050
import time

# MPU6050 sensörünün adresini tanımlayın (varsayılan olarak 0x68)
sensor_address = 0x68

# MPU6050 objesini oluşturun
mpu = mpu6050.mpu6050(sensor_address)

# Gyro ölçeğini ayarlayın (±250 dps)
mpu.set_gyro_range(mpu.GYRO_RANGE_250DEG)

# Fonksiyon ile sadece gyrodan veri okuyun
def read_gyro_data():
    gyro_data = mpu.get_gyro_data()
    gyro_x = gyro_data['x']
    gyro_y = gyro_data['y']
    gyro_z = gyro_data['z']
    return gyro_x, gyro_y, gyro_z

try:
    while True:
        gyro_x, gyro_y, gyro_z = read_gyro_data()
        print(f"Gyro X: {gyro_x}, Gyro Y: {gyro_y}, Gyro Z: {gyro_z}")
        time.sleep(0.1)  # 0.1 saniye bekleme

except KeyboardInterrupt:
    print("Program sonlandırıldı.")
