import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QTabWidget,QAction, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import cv2
import matplotlib.pyplot as plt
import numpy as np

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import sys
from PIL import Image
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMessageBox

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from math import cos, sin, radians

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QInputDialog
from PyQt5.QtGui import QPixmap, QImage, QTransform
from PyQt5.QtCore import Qt

import numpy as np
from PIL import Image

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

        # İç sekme 3 oluştur
        inner_tab3 = InnerTab3()

        # İç sekme 4 oluştur
        inner_tab4 = InnerTab4()

        # İç sekme widget'ını içindeki sekme widget'ına ekle
        self.inner_tab_widget.addTab(inner_tab1, "Görüntü Boyutu Büyütme")
        self.inner_tab_widget.addTab(inner_tab2, "Görüntü Boyutu Küçültme")
        self.inner_tab_widget.addTab(inner_tab3, "Zoom In & Zoom Out")
        self.inner_tab_widget.addTab(inner_tab4, "Görüntü Döndürme")


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
        global file_path
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
        yeni_resim = self.resmi_buyut(file_path, yeniOran)

        # Yeni resmi göster
        plt.imshow(yeni_resim)  # Yeni resmi plt ile göster
        plt.show()  # plt ile ekranı göster

    def resmi_buyut(self ,yol, oran):
        # Resmin boyutlarını al
        image = Image.open(yol)
        print("1")

        # Giriş resminin boyutları
        width, height = image.size
        print(width)
        print(height)


        # Yeni boyutları hesapla
        new_height = int(height * oran)
        new_width = int(width * oran)
        print("2")

        # Yeni boyutlarda bir ızgara oluştur
        new_y = np.arange(new_height).reshape(-1, 1).repeat(new_width, axis=1)
        new_x = np.arange(new_width).reshape(1, -1).repeat(new_height, axis=0)
        print("3")

        # Eski boyutlarda piksel koordinatlarını hesapla
        old_y = new_y / oran
        old_x = new_x / oran
        print("4")

        # Hesaplanan koordinatları birleştir
        points = np.stack([old_y, old_x], axis=-1)
        print("5")

        # Resmi NumPy dizisine dönüştür
        image_array = np.array(image)

        # Sıfırlar dizisi oluştur
        interpolated_image = np.zeros((new_height, new_width, image_array.shape[2]), dtype=np.uint8)

        # Yeni boyutlardaki her piksel için interpolasyon yap
        for i in range(new_height):
            for j in range(new_width):
                # Hesaplanan koordinatlar için dört komşu pikselin indekslerini hesapla
                y1, x1 = int(old_y[i, j]), int(old_x[i, j])
                y2, x2 = min(y1 + 1, height - 1), min(x1 + 1, width - 1)

                # Dört komşu pikselin değerlerini al
                q11, q12 = image_array[y1, x1], image_array[y1, x2]
                q21, q22 = image_array[y2, x1], image_array[y2, x2]

                # Bilinear interpolasyon formülü
                interpolated_value = (q11 * (x2 - old_x[i, j]) * (y2 - old_y[i, j]) +
                                      q21 * (old_x[i, j] - x1) * (y2 - old_y[i, j]) +
                                      q12 * (x2 - old_x[i, j]) * (old_y[i, j] - y1) +
                                      q22 * (old_x[i, j] - x1) * (old_y[i, j] - y1))

                # Hesaplanan interpolasyon değerini atama
                interpolated_image[i, j, :] = interpolated_value

        # Değerleri 0-255 aralığına kısıtlama
        interpolated_image = np.clip(interpolated_image, 0, 255).astype(np.uint8)
        print("6")
        # Interpolasyon sonucunu PIL görüntüsüne dönüştür
        interpolated_image_pil = Image.fromarray(interpolated_image)

        # Kaydet
        interpolated_image_pil.save("temp.jpg")
        return interpolated_image

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
        global file_path
        yolu = "C:/Users/esrat/Dersler/BaharDonemi/DijitalGoruntuIsleme/Hafta4/Odev/Odev/image/1.jpg"
        print(file_path)
        pencere = ResimKucultme(self)

class ResimKucultme(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Resim Kucultme')


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
        global file_path
        print(file_path)
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
        yeni_resim = self.resmi_kucult(file_path, yeniOran)

        # Yeni resmi göster
        plt.imshow(yeni_resim)  # Yeni resmi plt ile göster
        plt.show()  # plt ile ekranı göster

    def resmi_kucult(self, yol, oran):
        # Resmin boyutlarını al
        image = Image.open(yol)
        print("1")

        # Giriş resminin boyutları
        width, height = image.size
        print(width)
        print(height)

        # Yeni boyutları hesapla
        new_height = int(height * oran)
        new_width = int(width * oran)
        print("2")

        # Yeni boyutlarda bir ızgara oluştur
        new_y = np.arange(new_height).reshape(-1, 1).repeat(new_width, axis=1)
        new_x = np.arange(new_width).reshape(1, -1).repeat(new_height, axis=0)
        print("3")

        # Eski boyutlarda piksel koordinatlarını hesapla
        old_y = new_y / oran
        old_x = new_x / oran
        print("4")

        # Hesaplanan koordinatları birleştir
        points = np.stack([old_y, old_x], axis=-1)
        print("5")

        # Resmi NumPy dizisine dönüştür
        image_array = np.array(image)

        # Sıfırlar dizisi oluştur
        interpolated_image = np.zeros((new_height, new_width, image_array.shape[2]), dtype=np.uint8)

        # Yeni boyutlardaki her piksel için interpolasyon yap
        for i in range(new_height):
            for j in range(new_width):
                # Hesaplanan koordinatlar için dört komşu pikselin indekslerini hesapla
                y1, x1 = int(old_y[i, j]), int(old_x[i, j])
                y2, x2 = min(y1 + 1, height - 1), min(x1 + 1, width - 1)

                # Dört komşu pikselin değerlerini al
                q11, q12 = image_array[y1, x1], image_array[y1, x2]
                q21, q22 = image_array[y2, x1], image_array[y2, x2]

                # Bilinear interpolasyon formülü
                interpolated_value = (q11 * (x2 - old_x[i, j]) * (y2 - old_y[i, j]) +
                                      q21 * (old_x[i, j] - x1) * (y2 - old_y[i, j]) +
                                      q12 * (x2 - old_x[i, j]) * (old_y[i, j] - y1) +
                                      q22 * (old_x[i, j] - x1) * (old_y[i, j] - y1))

                # Hesaplanan interpolasyon değerini atama
                interpolated_image[i, j, :] = interpolated_value

        # Değerleri 0-255 aralığına kısıtlama
        interpolated_image = np.clip(interpolated_image, 0, 255).astype(np.uint8)
        print("6")
        # Interpolasyon sonucunu PIL görüntüsüne dönüştür
        interpolated_image_pil = Image.fromarray(interpolated_image)

        # Kaydet
        interpolated_image_pil.save("temp.jpg")
        return interpolated_image

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

class InnerTab3(QWidget):
    def __init__(self):
        super().__init__()
        window = ZoomApp(self)


class ZoomApp(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Zoom In & Zoom Out")
        self.setGeometry(100, 100, 640, 480)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(500, 500)  # Etiketin boyutunu 1000x1000 piksel olarak ayarla

        self.image_path = "C:/Users/esrat/Dersler/BaharDonemi/DijitalGoruntuIsleme/Hafta4/Odev2/image/1.jpg"  # Örnek olarak bir resim dosyası
        self.load_image()

        pixmap = QPixmap(self.image_path)
        self.newWidth = int(pixmap.width())  # İstediğiniz oranda büyütme faktörü (örneğin, 1.2)
        self.newHeight = int(pixmap.height())

        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.clicked.connect(self.zoom_in)

        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.clicked.connect(self.zoom_out)

        # Dikey düzen oluştur ve önce butonları, sonra resmi ekleyin
        layout = QVBoxLayout()
        layout.addWidget(self.zoom_in_button)
        layout.addWidget(self.zoom_out_button)
        layout.addStretch()
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignTop)  # Resmin üstte hizalanmasını sağla
        self.setLayout(layout)

    def load_image(self):
        pixmap = QPixmap(self.image_path)

        label_width = min(pixmap.width(), self.width())
        label_height = min(pixmap.height(), self.height())

        self.label.setPixmap(pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio))

    def zoom_in(self):
        pixmap = QPixmap(self.image_path)
        self.newWidth = int(self.newWidth * 1.1)  # İstediğiniz oranda büyütme faktörü (örneğin, 1.2)
        self.newHeight = int(self.newHeight * 1.1)
        self.label.setPixmap(self.scale_image(pixmap, self.newWidth, self.newHeight))

    def zoom_out(self):
        pixmap = QPixmap(self.image_path)
        self.newWidth = int(self.newWidth * 0.9)  # İstediğiniz oranda küçültme faktörü (örneğin, 1.2)
        self.newHeight = int(self.newHeight * 0.9)
        self.label.setPixmap(self.scale_image(pixmap, self.newWidth, self.newHeight))

    def scale_image(self, pixmap, width, height):
        scaled_image = QImage(width, height, QImage.Format_RGB32)
        for y in range(height):
            for x in range(width):
                new_x = int(x * pixmap.width() / width)
                new_y = int(y * pixmap.height() / height)
                color = pixmap.toImage().pixelColor(new_x, new_y)
                scaled_image.setPixelColor(x, y, color)
        return QPixmap.fromImage(scaled_image)


class InnerTab4(QWidget):
    def __init__(self):
        super().__init__()
        global file_path
        yolu = "C:/Users/esrat/Dersler/BaharDonemi/DijitalGoruntuIsleme/Hafta4/Odev/Odev/image/1.jpg"
        print(file_path)
        pencere = ImageRotateApp(self)

class ImageRotateApp(QWidget):
    def __init__(self,parent):
        super().__init__(parent)

        self.setWindowTitle("Image Rotation")
        self.setGeometry(50, 50, 640, 480)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(500, 500)  # Etiketin boyutunu 1000x1000 piksel olarak ayarla

        self.image_path = "C:/Users/esrat/Dersler/BaharDonemi/DijitalGoruntuIsleme/Hafta4/Odev2/image/1.jpg"  # Örnek olarak bir resim dosyası
        self.load_image()

        self.rotate_button = QPushButton("Döndür")
        self.rotate_button.clicked.connect(self.rotate_image)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.rotate_button)
        self.setLayout(layout)


    def load_image(self):
        pixmap = QPixmap(self.image_path)
        self.label.setPixmap(pixmap)
        self.label.setPixmap(pixmap.scaledToWidth(600))  # Pixmap'i genişliği 400 piksele ölçekle
        self.label.adjustSize()

    def rotate_image(self):
        angle, ok = QInputDialog.getInt(self, "Açı Girin", "Döndürme açısını girin:", 0, -360, 360)
        if ok:
            rotated_pixmap = self.rotate_pixmap(self.label.pixmap(), angle)
            self.label.setPixmap(rotated_pixmap)

    def rotate_pixmap(self, pixmap, angle):
        width = pixmap.width()
        height = pixmap.height()
        rotated_pixmap = QPixmap(width, height)
        rotated_pixmap.fill(Qt.transparent)  # Arka planı şeffaf yap
        rotated_image = QImage(width, height, QImage.Format_RGB32)

        # Açıyı radian cinsine dönüştür
        theta = radians(angle)

        for y in range(height):
            for x in range(width):
                # Yeni konumları hesapla
                new_x = int((x - width / 2) * cos(theta) - (y - height / 2) * sin(theta) + width / 2)
                new_y = int((x - width / 2) * sin(theta) + (y - height / 2) * cos(theta) + height / 2)

                # Yeni konum içindeyse, pikselin rengini kopyala
                if 0 <= new_x < width and 0 <= new_y < height:
                    color = pixmap.toImage().pixelColor(x, y)
                    rotated_image.setPixelColor(new_x, new_y, color)

        return QPixmap.fromImage(rotated_image)



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
