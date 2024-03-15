import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage


class ZoomApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zoom In & Zoom Out")
        self.setGeometry(100, 100, 640, 480)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.label = QLabel(self.central_widget)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(1000, 1000)  # Etiketin boyutunu 400x400 piksel olarak ayarla

        self.image_path = "C:/Users/esrat/Dersler/BaharDonemi/DijitalGoruntuIsleme/Hafta3/Odev2/image/1.jpg"  # Örnek olarak bir resim dosyası
        self.load_image()

        pixmap = QPixmap(self.image_path)
        self.newWidth = int(pixmap.width())  # İstediğiniz oranda büyütme faktörü (örneğin, 1.2)
        self.newHeight = int(pixmap.height())

        self.zoom_in_button = QPushButton("Zoom In",self.central_widget)
        self.zoom_in_button.clicked.connect(self.zoom_in)

        self.zoom_out_button = QPushButton("Zoom Out",self.central_widget)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.label)
        layout.addWidget(self.zoom_in_button)
        layout.addWidget(self.zoom_out_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZoomApp()
    window.show()
    sys.exit(app.exec_())
