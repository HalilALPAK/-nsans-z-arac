import colorDetection as color
import time
import cv2
import GPS as gps
import enKisaMesafe as ekm
import aci
import yonKontrol
import hareket
import mesafeSensor

def get_gps_data():
    return gps.gps_verileri_oku()


def mesafe_hesapla():
    return ekm.mesafee()


def aci_al():
    return aci.ara_aci()


def get_yaw():
    return aci.yaw_al()


def get_sensor_data():
    return mesafeSensor.mesafe()


def engelden_kac(detected_objects):
    for obj in detected_objects:
        label, x, y, width, height, rotation = obj
        if label == "Red":
            print(f"{label}: Object Coordinates - x: {x}, y: {y}, width: {width}, height: {height}, rotation: {rotation}")
            print("Sağa dön")
            hareket.saga_don(2000, 1000, 3)     # düzenle bunu
            # motora ona göre güç ver
        elif label == "Green":
            print(f"{label}: Object Coordinates - x: {x}, y: {y}, width: {width}, height: {height}, rotation: {rotation}")
            print("Sola dön")
            hareket.sola_don(1000, 2000, 3)     # düzenle bunu
        elif label == "Yellow":
            print(f"{label}: Object Coordinates - x: {x}, y: {y}, width: {width}, height: {height}, rotation: {rotation}")
            if x < 320:
                print("Sarı nesne kameranın solunda, sağa yönel")
                hareket.saga_don(2000, 1000, 3)     # düzenle bunu
            elif x > 640:
                print("Sarı nesne kameranın sağında, sola yönel")
                hareket.sola_don(1000, 2000, 3)     # düzenle bunu
            else:
                print("Sarı nesne kameranın ortasında, zikzak yönel")
                hareket.zigzag1(1000, 1000, 3, 3)     # düzenle bunu


if __name__ == "__main__":
    # nesne tespit etme
    while True:
        distance = get_sensor_data()
        if distance == 1:  # engel varsa
            detected_objects = color.color_detect()
            if detected_objects:  # Detected objects boş değilse
                engelden_kac(detected_objects)
                yonKontrol.yon_kontrol()
                hareket.send_rc_channels_override(1500, 1500)
            else:  # Detected objects boşsa
                print("No objects detected")
            cap = cv2.VideoCapture(0)  # Kamerayı tekrar aç
            if not cap.isOpened():
                break
        else:     # engel yoksa
            print("2 metre uzaklıkta nesne tespit edilmedi")
            gps_data = get_gps_data()
            print(gps_data)
            min_distance = mesafe_hesapla()
            print(min_distance)
            if not min_distance == 0:  # hedefe gelmemişsek engelden kaçma görevi devam eder
                yonKontrol.yon_kontrol()
                hareket.send_rc_channels_override(1500, 1500)  # degerleri değiştir teste göre
            else:  # hedefe ulaşıldı görev1 bitti
                print("engelden kacma görevi bitti!")
                break
        time.sleep(1)