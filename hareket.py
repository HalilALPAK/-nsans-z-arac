# bu kodda manuel modun aktif olması gerekebilir şimdilik es geçildi. 
#çalışması beklenmiyor
import time;
from pymavlink import mavutil
## gerekli yerler import edildi
master = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)
#bağlanıldı mastera atandı
def hareketet(master,x,y,z,r,t): 
    buttons = 1 + 1 << 3 + 1 << 7
    for i in range(0,t):
        master.mav.manual_control_send(
            master.target_system,
            x,#yatay
            y,#dikey
            z,#yükseklik
            r,#dönme yönü pozitif ise sağ
            buttons
            )
        time.sleep(1)
        
hareketet(master,10,10,10,10,10)        