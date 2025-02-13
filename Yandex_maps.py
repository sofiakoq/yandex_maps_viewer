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
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            "z": self.map_zoom
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
