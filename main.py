import sys
import requests
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap


class AppMapAPI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.map_api_server = "https://static-maps.yandex.ru/v1"
        self.map_api_key = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
        self.coords = ','.join(reversed(self.lineEdit.text().split(', ')))
        self.z = 12
        self.pushButton.clicked.connect(self.GetCoord)

    def GetCoord(self):
        self.coords = ','.join(reversed(self.lineEdit.text().split(', ')))
        self.GetMap(12)

    def GetMap(self, z):
        map_params = {"ll": self.coords, 'size': '400,400', 'z': z, "apikey": self.map_api_key}
        map_response = requests.get(self.map_api_server, params=map_params)
        f = open('bufer.png', 'wb+').write(map_response.content)
        self.imageLabel.setPixmap(QPixmap('bufer.png'))

    def keyPressEvent(self, event):
        if event.key() == 16777239 and self.z > 0:
            self.z -= 1
            self.GetMap(self.z)
        elif event.key() == 16777238 and self.z < 21:
            self.z += 1
            self.GetMap(self.z)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = AppMapAPI()
    ex.show()
    sys.exit(app.exec())
