import aci
import hedefKoordinat as hedef
import arm
import hareket


def yon_kontrol():
    hedef_x = hedef
    hedef_y = hedef

    aci_ = 450 - aci.ara_aci(hedef_x, hedef_y)

    yaw = aci.yaw_al()

    # iki fonksiyonda doğru arm edilecek deneyip iyi olan seçilecek şimdilik ilki seçildi
    arm.arm_et(1)
    # armanddisarm(1)


    def en_kucuk_aci(yaw):
        # İki açı arasındaki farkı bulun
        fark = abs(aci_ - yaw)

        # Eğer fark 180 dereceden büyükse, farkı 360 dereceye çıkarın
        if fark > 180:
            fark = 360 - fark

        return fark


    o = en_kucuk_aci()

    if (yaw >= 180):
        if (o >= 180):
            hareket.sola_dön(1300, 1500, 5)  # (sol,sağ,zaman)
            return 1
        else:
            hareket.sağa_dön(1500, 1300, 5)
            return 0
    else:
        if (o >= 180):
            hareket.sağa_dön(1500, 1300, 5)
            return 0
        else:
            hareket.sola_dön(1300, 1500, 5)
            return 1
        # gerekli denemelerler hangi açı için hangideğerler girilmei test edilerek öğrenilecek

if __name__ == "__main__":
    yon_kontrol()

