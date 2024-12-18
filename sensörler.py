import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Sensörlerin pin numaralarını tanımlayalım
sensorler = {
    'on': {'TRIG': 23, 'ECHO': 24},
    'sag': {'TRIG': 27, 'ECHO': 22},
    'sol': {'TRIG': 5, 'ECHO': 6},
    'arka': {'TRIG': 13, 'ECHO': 19}
}

# Tüm sensörler için pin ayarlarını yapalım
for sensor in sensorler.values():
    GPIO.setup(sensor['TRIG'], GPIO.OUT)
    GPIO.setup(sensor['ECHO'], GPIO.IN)

def mesafe_olc(sensor_adi,olcu):
    if sensor_adi not in sensorler:
        print("Geçersiz sensör ")
        return None

    TRIG = sensorler[sensor_adi]['TRIG']
    ECHO = sensorler[sensor_adi]['ECHO']

    GPIO.output(TRIG, False)
    time.sleep(0.5)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_suresi = pulse_end - pulse_start
    mesafe = pulse_suresi * 17150
    mesafe = round(mesafe, 2)

    if mesafe < olcu:
        print(f"{sensor_adi} Mesafe:", mesafe - 0.5, "cm")
        return 1
    else:
        print(f"{sensor_adi} Menzil asildi")
        return 0

# Örnek kullanım
mesafe_olc('on')
mesafe_olc('sag')
mesafe_olc('sol')
mesafe_olc('arka')

# GPIO temizleme işlemi
GPIO.cleanup()
