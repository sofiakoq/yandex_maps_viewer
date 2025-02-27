import sys
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
import requests
import os


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('map_viewer.ui', self)
        self.api_srver = 'https://static-maps.yandex.ru/1.x/'
        self.map_zoom = 8
        self.delta = 0.1
        self.map_ll = [37.621601, 55.753460]
        self.map_l = 'map'
        self.theme = 'light'
        self.map_type = 'map'
        self.apikey = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        self.refresh_map()
        self.pushButton_5.clicked.connect(self.change_theme)
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.set_map)
        self.pushButton_3.clicked.connect(self.set_sat)
        self.pushButton_4.clicked.connect(self.set_hybrid)

    def search(self):
        pass

    def set_map(self):
        self.map_type = 'map'
        self.refresh_map()

    def set_sat(self):
        self.map_type = 'driving'
        self.refresh_map()

    def set_hybrid(self):
        self.map_type = 'transit'
        self.refresh_map()

    def change_theme(self):
        if self.theme == 'light':
            self.theme = 'dark'
        else:
            self.theme = 'light'
        self.refresh_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp and self.map_zoom <= 20:
            self.map_zoom += 1
        if event.key() == Qt.Key.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        if event.key() == Qt.Key.Key_A:
            self.map_ll[0] -= self.delta
        if event.key() == Qt.Key.Key_D:
            self.map_ll[0] += self.delta
        if event.key() == Qt.Key.Key_W:
            self.map_ll[1] += self.delta
        if event.key() == Qt.Key.Key_S:
            self.map_ll[1] -= self.delta
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            "z": self.map_zoom,
            "theme": self.theme,
            "apikey": self.apikey,
            "maptype": self.map_type
        }
        response = requests.get(self.api_srver, params=map_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
