
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import sys
from PIL import Image
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMessageBox


class ResimKucultme(QWidget):
    def __init__(self, yol):
        super().__init__()
        self.setWindowTitle('Resim Kucultme')

        self.yol = yol

        # Kullanıcı arayüzü bileşenlerini oluştur
        self.etiket = QLabel("Ne kadar küçültmek istersiniz:")
        self.giris = QLineEdit()
        self.buton = QPushButton("Küçült")
        self.buton.clicked.connect(self.resmi_kucult_ve_goster)

        # Arayüzü düzenle
        layout = QVBoxLayout()
        layout.addWidget(self.etiket)
        layout.addWidget(self.giris)
        layout.addWidget(self.buton)
        self.setLayout(layout)

    def resmi_kucult_ve_goster(self):
        try:
            oran = float(self.giris.text())
            yeniOran = 1 / oran
            if oran <= 0:
                QMessageBox.warning(self, "Hata", "Oran pozitif bir sayı olmalıdır.")
                return
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçersiz oran.")
            return

        # Resmi büyüt
        yeni_resim = self.resmi_kucult(self.yol, yeniOran)

        # Yeni resmi göster
        yeni_resim.show()

    def resmi_kucult(self ,yol, oran):
        # Resmi aç
        resim = Image.open(yol)
        orijinal_genislik, orijinal_yukseklik = resim.size

        # Yeni boyutları hesapla
        yeni_genislik = int(orijinal_genislik * oran)
        yeni_yukseklik = int(orijinal_yukseklik * oran)

        # Yeni boyutta bir boş resim oluştur
        yeni_resim = Image.new("RGB", (yeni_genislik, yeni_yukseklik))

        # Yeni resmin piksellerini oluştur
        for y in range(yeni_yukseklik):
            for x in range(yeni_genislik):
                # Orjinal resimdeki pikselin koordinatlarını hesapla
                orijinal_x = int(x / oran)
                orijinal_y = int(y / oran)

                # Orjinal resimdeki pikselin rengini al
                renk = resim.getpixel((orijinal_x, orijinal_y))

                # Yeni resimde pikselin rengini ayarla
                yeni_resim.putpixel((x, y), renk)

        # Resmi yeniden boyutlandır
        #yeni_resim = resim.resize((yeni_genislik, yeni_yukseklik), Image.Resampling.LANCZOS)

        # PIL resmini QPixmap'e dönüştür
        yeni_resim.save("temp.jpg")
        pixmap = QPixmap("temp.jpg")

        return yeni_resim



if __name__ == '__main__':
    app = QApplication(sys.argv)

    yolu = "C:/Users/esrat/Dersler/BaharDonemi/DijitalGoruntuIsleme/Hafta3/Odev2/image/1.jpg"
    oran = 2  # Resmi orijinal boyutunun %50'sine küçült
    # pencere = ResimBuyutme(yolu, oran)
    pencere = ResimKucultme(yolu)
    pencere.show()

    sys.exit(app.exec_())

