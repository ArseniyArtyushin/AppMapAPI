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
        self.pushButton.clicked.connect(self.GetMap)

    def GetMap(self):
        coordinates = ','.join(reversed(self.lineEdit.text().split(', ')))
        map_params = {"ll": coordinates, "z": '12', "apikey": self.map_api_key}
        map_response = requests.get(self.map_api_server, params=map_params)
        print(map_response)
        f = open('bufer.png', 'wb+').write(map_response.content)
        self.imageLabel.setPixmap(QPixmap('bufer.png'))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = AppMapAPI()
    ex.show()
    sys.exit(app.exec())
