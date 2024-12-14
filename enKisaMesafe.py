#gpsteki veriler alınınp hesaba katılmalı ama önce iha haberleşmesi yapılmalı
import GPS as gps
import math


def mesafee(iha_a,iha_b):
    a,b,c= gps.gps_verileri_oku()
    return math.sqrt(float((iha_a-a)**2)+float((iha_b-b)**2))

mesafee()