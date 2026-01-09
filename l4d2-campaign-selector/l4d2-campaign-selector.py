from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QSizePolicy, QVBoxLayout, QLabel, 
                             QHBoxLayout, QGraphicsDropShadowEffect, QGraphicsEffect, QTextEdit,
                             QGridLayout, QPushButton)
from PyQt5.QtCore import Qt, QPropertyAnimation, QPointF, QTimer, QDateTime, QDate, pyqtSignal, QUrl, QSize
from PyQt5.QtGui import QFont, QLinearGradient, QPainter, QBrush, QPen, QColor, QPixmap, QDesktopServices
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from datetime import datetime
# from l4d2_campaign_selector.decide_campaign import ModDecider
from decide_campaign import ModDecider

# Add a container widget to the thumbnail so that the mod url only open when you click directly on the image and not the borders of the widget
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_window_properties()
        self.initUI() 

        self.mod_thumbnail_label.clicked.connect(self.open_mod_url)

        # self.mod_decider = ModDecider()

        # self.set_mod_description_label()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)

        self.create_mod_title_label(main_layout=main_layout)
        self.create_mod_thumbnail_label(main_layout=main_layout)
        self.create_mod_rating_label(main_layout=main_layout)
        self.create_mod_description_label(main_layout=main_layout)
        self.create_buttons(main_layout=main_layout)
    
    def set_window_properties(self):
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #1E0000")
        self.setContentsMargins(100, 0, 100, 0)
        self.showMaximized()

    def create_mod_title_label(self, main_layout):
        self.mod_title_label = QLabel("Ice Canyon")
        self.mod_title_label.setAlignment(Qt.AlignCenter)
        self.mod_title_label.setFont(QFont("Chewy", 25))
        self.mod_title_label.setStyleSheet("""
            color: #F2F2E6; 
            background-color: #2A2A2A; 
            border: 2px solid #4A1A1A
        """)

        main_layout.setRowStretch(0, 1)
        main_layout.addWidget(self.mod_title_label, 0, 0, 1, 2)

    def create_mod_thumbnail_label(self, main_layout):
        # mod_thumbnail_container = QWidget()
        # container_layout = QVBoxLayout()
        # mod_thumbnail_container.setLayout(container_layout)

        self.mod_thumbnail_label = ClickableQLabel()
        self.mod_thumbnail_label.setAlignment(Qt.AlignCenter)
        self.mod_thumbnail_label.setStyleSheet("""
                                               ClickableQLabel {
                                                background-color: #2A2A2A;
                                                border: 2px solid #4A1A1A
                                               }
                                               ClickableQLabel:hover {
                                                background-color: #3E3E3E
                                               }
                                               """)

        # mod_thumbnail = QPixmap("l4d2_campaign_selector/ice_canyon.jpg")
        # mod_thumbnail_size = QSize(int(self.mod_thumbnail_label.width() * 0.85), int(self.mod_thumbnail_label.height() * 0.85))
        # mod_thumbnail = mod_thumbnail.scaled(mod_thumbnail_size, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        # self.mod_thumbnail_label.setPixmap(mod_thumbnail)

        # mod_thumbnail_container.setFixedSize(self.mod_thumbnail_label.width(), self.mod_thumbnail_label.height())
        
        main_layout.addWidget(self.mod_thumbnail_label, 1, 0, 2, 1)
        # main_layout.addWidget(mod_thumbnail_container, 1, 0, 2, 1)
        # container_layout.addWidget(self.mod_thumbnail_label)

    def create_mod_rating_label(self, main_layout):
        mod_rating_image = QPixmap("l4d2_campaign_selector/4-star.png")
        mod_rating_image = mod_rating_image.scaled(self.mod_thumbnail_label.width(), self.mod_thumbnail_label.height(), Qt.KeepAspectRatio, Qt.FastTransformation)

        self.mod_rating_label = QLabel()
        self.mod_rating_label.setPixmap(mod_rating_image)
        self.mod_rating_label.setAlignment(Qt.AlignCenter)
        self.mod_rating_label.setStyleSheet("""
            background-color: #2A2A2A; 
            border: 2px solid #4A1A1A;
            padding-right: 15px; 
            padding-left: 15px; 
            padding-top: 15px; 
            padding-bottom: 15px
        """)

        main_layout.addWidget(self.mod_rating_label, 1, 1, 1, 1)
        main_layout.setRowStretch(1, 1)

    def create_mod_description_label(self, main_layout):
        # self.mod_description_label = QLabel()
        self.mod_description_label = QLabel("\"The road is covered with snow, so the survivors will have to make their way through the icy canyon in search of salvation.\" Hello friends! Last December, I created the \"Ice Canyon\" map for the game Battle Grounds III. I decided to use it as a basis and cr...")
        self.mod_description_label.setFont(QFont("Chewy", 25))
        self.mod_description_label.setAlignment(Qt.AlignTop)
        self.mod_description_label.setWordWrap(True)
        self.mod_description_label.setStyleSheet("""
            background-color: #8B0000; 
            color: #F2F2E6; 
            padding-right: 20px; 
            padding-left: 20px; 
            padding-top: 20px; 
            padding-bottom: 20px
        """)

        main_layout.setRowStretch(2, 10)
        main_layout.addWidget(self.mod_description_label, 2, 1, 1, 1)

    def create_buttons(self, main_layout):
        self.no_button = QPushButton("No")
        self.no_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.no_button.setFont(QFont("Chewy", 20))
        self.no_button.setStyleSheet("""
                                     QPushButton {
                                        background-color: #6C3434; 
                                        color: #F2F2E6
                                     }
                                     QPushButton:hover {
                                        background-color: #804848
                                     }
                                     QPushButton:pressed {
                                        background-color: #582020
                                     }
                                     """)
        main_layout.addWidget(self.no_button, 3, 0, 1, 1)

        self.yes_button = QPushButton("Yes")
        self.yes_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.yes_button.setFont(QFont("Chewy", 20))
        self.yes_button.setStyleSheet("""
                                      QPushButton {
                                        background-color: #B05454; 
                                        color: #F2F2E6
                                      }
                                      QPushButton:hover {
                                        background-color: #C46868
                                      }
                                      QPushButton:pressed {
                                        background-color: #9C4040
                                      }
                                      """)
        main_layout.addWidget(self.yes_button, 3, 1, 1, 1)
        main_layout.setRowStretch(3, 1)

        self.maybe_button = QPushButton("Maybe")
        self.maybe_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.maybe_button.setFont(QFont("Chewy", 20))
        self.maybe_button.setStyleSheet("""
                                        QPushButton {
                                            background-color: #8E4444; 
                                            color: #F2F2E6
                                        }
                                        QPushButton:hover {
                                            background-color: #A25858
                                        }
                                        QPushButton:pressed {
                                            background-color: #7A3030
                                        }
                                        """)
        main_layout.addWidget(self.maybe_button, 4, 0, 1, 2)
        main_layout.setRowStretch(4, 1)

    def open_mod_url(self):
        """Opens the current mod's url in your browser."""
        QDesktopServices.openUrl(QUrl("https://steamcommunity.com/sharedfiles/filedetails/?id=3634176047&searchtext="))

    def resize_mod_thumbnail(self):
        if hasattr(self, "mod_thumbnail_label") == True:
            self.set_mod_thumbnail_image()

    def resizeEvent(self, a0):
        self.resize_mod_thumbnail()

        return super().resizeEvent(a0)

    def set_mod_thumbnail_image(self):
        mod_thumbnail = QPixmap("l4d2_campaign_selector/ice_canyon.jpg")
        mod_thumbnail_size = QSize(int(self.mod_thumbnail_label.width() * 0.85), int(self.mod_thumbnail_label.height() * 0.85))
        mod_thumbnail = mod_thumbnail.scaled(mod_thumbnail_size, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.mod_thumbnail_label.setPixmap(mod_thumbnail)

    # def set_mod_description_label(self):
    #     self.mod_decider.all_mods

class ClickableQLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)

    clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()
        return super().mousePressEvent(ev)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()

# manager = QNetworkAccessManager()
# url = "https://images.steamusercontent.com/ugc/11267625434000555311/D397044B8584358CDE1D1DBB16EFF40B60F8B430/?imw=200&imh=200&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true"
# request = QNetworkRequest(url)
# reply = manager.get(request)
