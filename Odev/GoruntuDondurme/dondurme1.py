import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QInputDialog
from PyQt5.QtGui import QPixmap, QImage, QTransform
from PyQt5.QtCore import Qt

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from math import cos, sin, radians

class ImageRotateApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Rotation")
        self.setGeometry(100, 100, 640, 480)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.label = QLabel(self.central_widget)
        self.label.setAlignment(Qt.AlignCenter)

        # Label'ı şeffaf yap

        self.image_path = "C:/Users/esrat/Dersler/BaharDonemi/DijitalGoruntuIsleme/Hafta3/Odev2/image/1.jpg"  # Örnek olarak bir resim dosyası
        self.load_image()

        self.rotate_button = QPushButton("Döndür", self.central_widget)
        self.rotate_button.clicked.connect(self.rotate_image)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.label)
        layout.addWidget(self.rotate_button)

    def load_image(self):
        pixmap = QPixmap(self.image_path)
        self.label.setPixmap(pixmap)
        self.label.setPixmap(pixmap.scaledToWidth(400))  # Pixmap'i genişliği 400 piksele ölçekle
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageRotateApp()
    window.show()
    sys.exit(app.exec_())
