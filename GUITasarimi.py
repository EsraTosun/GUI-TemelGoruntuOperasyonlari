import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QTabWidget,QAction, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import Qt

import cv2
import matplotlib.pyplot as plt
import numpy as np

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import sys
from PIL import Image
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMessageBox

# Global değişken olarak file_path tanımlanıyor
file_path = None

class Odev1Page(QWidget):
    def __init__(self):
        super().__init__()
        # Histogramı tutacak değişkeni tanımla
        self.histogram_data = None
        self.image = None

        layout = QVBoxLayout(self)

        # Resim göstermek için bir QLabel oluştur
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        # Resmi yüklemek için bir buton oluştur
        self.load_image_button = QPushButton("Resim Yükle")
        self.load_image_button.clicked.connect(self.load_image)

        # Histogram oluşturmak için bir buton oluştur
        self.load_histogram_button = QPushButton("Histogram oluştur")
        self.load_histogram_button.clicked.connect(self.load_histogram)

        # Layout'a widget'ları ekle
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_image_button)
        layout.addWidget(self.load_histogram_button)

        # Histogram grafiği için bir QGraphicsView oluştur
        # self.histogram_view = pg.GraphicsView()
        # layout.addWidget(self.histogram_view)


    def load_image(self):
        global file_path  # global değişkene erişim sağlanıyor
        # Resim seçme işlemi için dosya iletişim kutusunu aç
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Resim dosyaları (*.jpg *.png)")
        file_dialog.setViewMode(QFileDialog.Detail)
        
        # Kullanıcı bir resim seçerse, resmi yükle
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(file_path)

            # Resmi boyutlandır
            pixmap = pixmap.scaledToWidth(1000)  # Genişliği 400 piksel olarak ayarla

            self.image_label.setPixmap(pixmap)

            # QPixmap'ı QImage'e dönüştür
            self.image = pixmap.toImage()

    def load_histogram(self):
        if self.image is not None:
            # QImage'i QPixmap'e dönüştür
            pixmap = QPixmap(self.image)

            # QPixmap'i QImage'e dönüştür
            qimage = pixmap.toImage()

            # QImage'i numpy dizisine dönüştür
            height, width = qimage.height(), qimage.width()
            ptr = qimage.bits()  # QByteArray al
            ptr.setsize(qimage.byteCount())  # QByteArray boyutunu ayarla
            arr = np.array(ptr).reshape(height, width, 4)  # 4 kanallı (RGBA) bir görüntü olduğunu varsayıyoruz

            # Görüntüyü BGR renk formatına dönüştür (OpenCV için gereklidir)
            bgr_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

            # Görüntüyü tek boyutlu bir numpy dizisine düzleştir
            flattened_image = bgr_image.ravel()

            # Histogramı oluştur
            plt.hist(flattened_image, bins=256, range=[0, 256])
            plt.show()


        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir resim yükleyin.")


class Odev2Page(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Ödev 2 sekmesi içinde başka bir QTabWidget oluştur
        self.inner_tab_widget = QTabWidget()

        # İç sekme widget'ını ödev 2 sayfasının ana layoutuna ekleyin
        layout.addWidget(self.inner_tab_widget)

        # İlk iç sekme oluştur
        self.create_inner_tabs()

    def create_inner_tabs(self):
        # İç sekme 1 oluştur
        inner_tab1 = InnerTab1()

        # İç sekme 2 oluştur
        inner_tab2 = InnerTab2()

        # İç sekme widget'ını içindeki sekme widget'ına ekle
        self.inner_tab_widget.addTab(inner_tab1, "Görüntü Boyutu Büyütme")
        self.inner_tab_widget.addTab(inner_tab2, "Sekme 2")

class InnerTab1(QWidget):
    def __init__(self):
        super().__init__()


        yolu = "C:/Users/esrat/Dersler/BaharDonemi/DijitalGoruntuIsleme/Hafta4/Odev/Odev/image/1.jpg"
        # pencere = ResimBuyutme(yolu, oran)
        pencere = ResimBuyutme(self,yolu)

class ResimBuyutme(QWidget):
    def __init__(self, parent, yol):
        super().__init__(parent)
        self.setWindowTitle('Resim Büyütme')

        self.parent = parent
        self.yol = yol

        # Kullanıcı arayüzü bileşenlerini oluştur
        self.etiket = QLabel("Ne kadar büyültmek istersiniz:")
        self.giris = QLineEdit()
        self.buton = QPushButton("Büyüt")
        self.buton.clicked.connect(self.resmi_buyut_ve_goster)

        # Arayüzü düzenle
        layout = QVBoxLayout()
        layout.addWidget(self.etiket)
        layout.addWidget(self.giris)
        layout.addWidget(self.buton)
        self.setLayout(layout)

    def resmi_buyut_ve_goster(self):
        try:
            oran = float(self.giris.text())
            if 0 < oran < 1:
                yeniOran = 1 + oran
            elif oran >= 1:
                yeniOran = oran
            else:
                QMessageBox.warning(self, "Hata", "Oran pozitif bir sayı olmalıdır.")
                return
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçersiz oran.")
            return

        # Resmi büyüt
        yeni_resim = self.resmi_buyut(self.yol, yeniOran)

        # Yeni resmi göster
        self.resmi_goster(yeni_resim)

    def resmi_buyut(self ,yol, oran):
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
        yeni_resim.save("temp.jpg")

        return "temp.jpg"

    def resmi_goster(self, yol):
        pixmap = QPixmap(yol)
        etiket = QLabel()
        etiket.setPixmap(pixmap)

        # Mevcut layoutu temizle
        self.layout().deleteLater()

        # Yeni bir QVBoxLayout oluştur
        yeni_layout = QVBoxLayout()
        yeni_layout.addWidget(etiket)

        # Widget'in layoutunu güncelle
        self.setLayout(yeni_layout)

class InnerTab2(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        label2 = QLabel("İç Sekme 2")
        layout.addWidget(label2)


class ImageProcessingWindow(QWidget):
    def __init__(self, image, parent=None):
        super().__init__(parent)

        # Görüntüyü göstermek için bir QLabel oluştur
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap.fromImage(image))

        # Histogram ve kanallar için etiketler oluştur
        self.histogram_label = QLabel("Histogram")
        self.channels_label = QLabel("Kanallar")
        
        # Layout oluştur ve widget'ları layouta ekle
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.histogram_label)
        layout.addWidget(self.channels_label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.histogram_tab = None  # histogram_tab değişkenini tanımlıyoruz

        # Ana pencere özelliklerini ayarla
        self.setWindowTitle("Dijital Görüntü İşleme")
        self.setGeometry(200, 200, 1000, 1000)

        # Ana widget oluştur
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Ana layout oluştur
        layout = QVBoxLayout(main_widget)

        # Başlık etiketi oluştur ve ana layouta ekle
        title_label = QLabel("Dijital Görüntü İşleme Uygulaması", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #344955; margin: 30px;")
        layout.addWidget(title_label)

        # Öğrenci bilgi etiketi oluştur ve ana layouta ekle
        student_info_label = QLabel("Numara: 2112290034\nAd Soyad: Esra Tosun", self)
        student_info_label.setAlignment(Qt.AlignCenter)
        student_info_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #50727B; margin: 15px;")
        layout.addWidget(student_info_label)

        # Arka plan rengini ayarla
        background_color = QColor("#78A083")
        main_widget.setStyleSheet(f"background-color: {background_color.name()};")

        # Ana pencere için sekme widget'ı oluştur ve ana layouta ekle
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Sekmeler oluştur
        self.create_odev1_page()
        self.create_odev2_page()
        self.create_histogram_page()

        # Menüleri oluştur
        self.create_actions()
        self.create_menu_navigation()

    def create_histogram_page(self):
        # Histogram sekmesi için bir QTabWidget oluştur
        self.histogram_tab = QTabWidget()
        
        # Ana tablo widget'ına histogram sekmesini ekleyin
        self.tab_widget.addTab(self.histogram_tab, "Histogram")

    def create_odev1_page(self):
        # Ana sekme oluştur ve sekme widget'ına ekle
        odev1_tab = Odev1Page()
        self.tab_widget.addTab(odev1_tab, "Ödev 1: Temel İşlevselliği Oluştur")

    def create_odev2_page(self):
        # Ödev2 sekmesini oluştur ve sekme widget'ına ekle
        odev2_tab = Odev2Page()
        self.tab_widget.addTab(odev2_tab, "Ödev 2: Temel Görüntü Operasyonları ve İnterpolasyon")

    def create_actions(self):
        # Yeni eylem oluştur ve tetikleyici ataması yap
        self.new_action = QAction("Yeni", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.new_image_processing_window)

    def create_menu_navigation(self):
        # Ana menü çubuğunu oluştur
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: #f0f0f0;")

        # Dosya menüsünü oluştur ve eylemi ekle
        file_menu = menubar.addMenu("Dosya")
        file_menu.addAction(self.new_action)

    def show_home_page(self):
        # Ana sayfaya git
        self.tab_widget.setCurrentIndex(0)

    def new_image_processing_window(self):
        # Yeni bir görüntü işleme penceresi oluştur
        image = QImage(640, 480, QImage.Format_RGB32)
        image.fill(Qt.white)  # Beyaz bir arka plan ekleyin
        image_processing_window = ImageProcessingWindow(image)
        
        # Histogram sekmesine yeni bir sayfa ekle
        self.histogram_tab.addTab(image_processing_window, "Yeni İşlem")




if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
