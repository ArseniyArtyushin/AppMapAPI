import sys
import requests
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QKeyEvent


class AppMapAPI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.map_api_server = "https://static-maps.yandex.ru/v1"
        self.map_api_key = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
        self.coords = ','.join(reversed(self.lineEdit.text().split(', ')))
        self.z = 12
        self.theme = True
        self.lineEdit.keyPressEvent = self.LEPressEvent
        self.pushButton.clicked.connect(self.GetCoord)
        self.pushSwitch.clicked.connect(self.ChangeTheme)

    def ChangeTheme(self):
        uic.loadUi(('main_black.ui' if self.theme else 'main.ui'), self)
        self.theme = False if self.theme else True
        self.GetMap()
        self.pushButton.clicked.connect(self.GetCoord)
        self.pushSwitch.clicked.connect(self.ChangeTheme)

    def GetCoord(self):
        self.coords = ','.join(reversed(self.lineEdit.text().split(', ')))
        self.GetMap()

    def GetMap(self):
        map_params = {"ll": self.coords, 'size': '400,400', 'z': self.z, "apikey": self.map_api_key,
                      'theme': ('light' if self.theme else 'dark')}
        map_response = requests.get(self.map_api_server, params=map_params)
        f = open('bufer.png', 'wb+').write(map_response.content)
        self.imageLabel.setPixmap(QPixmap('bufer.png'))

    def LEPressEvent(self, event: QKeyEvent):
        self.keyPressEvent(event)

    def keyPressEvent(self, event):
        if event.key() == 16777239 and self.z > 0:
            self.z -= 1
            self.GetMap()
        elif event.key() == 16777238 and self.z < 21:
            self.z += 1
            self.GetMap()
        elif event.key() == 16777234:
            self.coords = f"{float(self.coords.split(',')[0]) - 0.5},{self.coords.split(',')[1]}"
            self.lineEdit.setText(', '.join(reversed(self.coords.split(','))))
            self.GetMap()
        elif event.key() == 16777235:
            self.coords = f"{self.coords.split(',')[0]},{float(self.coords.split(',')[1]) + 0.25}"
            self.lineEdit.setText(', '.join(reversed(self.coords.split(','))))
            self.GetMap()
        elif event.key() == 16777236:
            self.coords = f"{float(self.coords.split(',')[0]) + 0.5},{self.coords.split(',')[1]}"
            self.lineEdit.setText(', '.join(reversed(self.coords.split(','))))
            self.GetMap()
        elif event.key() == 16777237:
            self.coords = f"{self.coords.split(',')[0]},{float(self.coords.split(',')[1]) - 0.25}"
            self.lineEdit.setText(', '.join(reversed(self.coords.split(','))))
            self.GetMap()
        else:
            print(event.key())
        print(True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = AppMapAPI()
    ex.show()
    sys.exit(app.exec())
