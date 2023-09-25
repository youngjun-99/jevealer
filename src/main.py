
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from riotclient import *
from scraper import SummonerInfoScraper
import webbrowser

scraper = SummonerInfoScraper()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1120, 920)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 40, 1100, 900))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.image.setObjectName("image")
        self.verticalLayout.addWidget(self.image)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 1100, 30))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.reveal = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.reveal.setObjectName("reveal")
        self.reveal.clicked.connect(self.reveal_btn_clicked)
        self.horizontalLayout.addWidget(self.reveal)
        self.go_github = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.go_github.setObjectName("go_github")
        self.go_github.clicked.connect(self.go_github_btn_clicked)
        self.horizontalLayout.addWidget(self.go_github)
        self.version_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.version_label.setObjectName("version_label")
        self.horizontalLayout.addWidget(self.version_label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Jeaveler"))
        self.reveal.setText(_translate("MainWindow", "팀 전적 확인"))
        self.go_github.setText(_translate("MainWindow", "Github"))
        self.version_label.setText(_translate("MainWindow", "Version: 1.0.1"))
        return
    
    def reveal_btn_clicked(self):
        riotclient_session_token, riotclient_app_port = asyncio.run(get_lcu())
        riotclient_headers = asyncio.run(get_headers(riotclient_session_token))
        summoners = asyncio.run(get_summoners(riotclient_app_port, riotclient_headers))
        scraper.driver.get(f'https://www.op.gg/multisearch/kr?summoners={summoners}')
        screenshot = scraper.get_image()
        pixmap = QPixmap()
        pixmap.loadFromData(screenshot)
        self.image.setPixmap(pixmap)
        return

    def go_github_btn_clicked(self):
        webbrowser.open('https://github.com/youngjun-99')
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())