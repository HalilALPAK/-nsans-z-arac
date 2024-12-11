#çalışıp çalışmadığından emin değilim
import RPi.GPIO as GPIO
import time

# Sızdırmazlık sensörünün bağlı olduğu GPIO pinini tanımla
sensor_pin = 8

# Raspberry Pi GPIO pinlerini başlat
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)

try:
    while True:
        # Sensörden veri al
        sensor_value = GPIO.input(sensor_pin)

        # Sensör değerine göre durumu kontrol et
        if sensor_value == GPIO.LOW:
            print("su algılandı!")  # Sızdırmazlık algılandığında yapılacak işlem
        else:
            print("Sızdırmazlık")  # Sızdırmazlık algılanmadığında yapılacak işlem

        time.sleep(1)  # 1 saniye bekle

except KeyboardInterrupt:
    GPIO.cleanup()
