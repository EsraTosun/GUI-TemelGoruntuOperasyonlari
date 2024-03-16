import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout

class ImageInterpolator:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = self.load_image()

    def load_image(self):
        # Görüntüyü yükle
        # Örnek olarak burada PIL kullanıyoruz
        from PIL import Image
        return np.array(Image.open(self.image_path))

    def bilinear_interpolation(self, new_height, new_width):
        height, width = self.image.shape[:2]
        new_image = np.zeros((new_height, new_width, self.image.shape[2]), dtype=np.uint8)

        # Yeni boyutların oranlarını hesapla
        x_ratio = float(width - 1) / new_width
        y_ratio = float(height - 1) / new_height

        for i in range(new_height):
            for j in range(new_width):
                x = int(x_ratio * j)
                y = int(y_ratio * i)
                dx = (x_ratio * j) - x
                dy = (y_ratio * i) - y

                # Bilinear interpolation formülü
                new_image[i, j] = (1 - dx) * (1 - dy) * self.image[y, x] + dx * (1 - dy) * self.image[y, x + 1] + \
                                  (1 - dx) * dy * self.image[y + 1, x] + dx * dy * self.image[y + 1, x + 1]

        return new_image

    def average_interpolation(self, new_height, new_width):
        height, width = self.image.shape[:2]
        new_image = np.zeros((new_height, new_width, self.image.shape[2]), dtype=np.uint8)

        # Yeni boyutların oranlarını hesapla
        x_ratio = float(width) / new_width
        y_ratio = float(height) / new_height

        for i in range(new_height):
            for j in range(new_width):
                x = int(x_ratio * j)
                y = int(y_ratio * i)

                # Average interpolation formülü
                new_image[i, j] = np.mean(self.image[y:y + int(y_ratio), x:x + int(x_ratio)], axis=(0, 1))

        return new_image

class InterpolationApp(QWidget):
    def __init__(self, image_path, bilinear_result, average_result):
        super().__init__()

        self.setWindowTitle("Interpolasyon Sonuçları")
        self.setGeometry(100, 100, 800, 600)

        layout = QHBoxLayout()

        # Bilinear Interpolasyon Sonucu
        bilinear_layout = QVBoxLayout()

        bilinear_label = QLabel()
        bilinear_label.setText("Bilinear Interpolasyon Sonucu")
        bilinear_layout.addWidget(bilinear_label)

        bilinear_text = QLabel()
        bilinear_text.setText(str(bilinear_result))
        bilinear_layout.addWidget(bilinear_text)

        layout.addLayout(bilinear_layout)

        # Average Interpolasyon Sonucu
        average_layout = QVBoxLayout()

        average_label = QLabel()
        average_label.setText("Average Interpolasyon Sonucu")
        average_layout.addWidget(average_label)

        average_text = QLabel()
        average_text.setText(str(average_result))
        average_layout.addWidget(average_text)

        layout.addLayout(average_layout)

        self.setLayout(layout)

# Örnek bir görüntü dosya yolu
image_path = "C:/Users/esrat/Dersler/BaharDonemi/DijitalGoruntuIsleme/Hafta4/Odev2/image/1.jpg"

# ImageInterpolator sınıfını kullanarak interpolasyon işlemlerini uygula
interpolator = ImageInterpolator(image_path)

new_height = 5
new_width = 5

# Bilinear interpolasyon uygula
bilinear_result = interpolator.bilinear_interpolation(new_height, new_width)

# Average interpolasyon uygula
average_result = interpolator.average_interpolation(new_height, new_width)


# PyQt5 uygulamasını başlat
app = QApplication(sys.argv)
ex = InterpolationApp(image_path, bilinear_result, average_result)
ex.show()
sys.exit(app.exec_())
