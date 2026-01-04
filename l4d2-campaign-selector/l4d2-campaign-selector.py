from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QSizePolicy, QVBoxLayout, QLabel, 
                             QHBoxLayout, QGraphicsDropShadowEffect, QGraphicsEffect, QTextEdit,
                             QGridLayout, QPushButton)
from PyQt5.QtCore import Qt, QPropertyAnimation, QPointF, QTimer, QDateTime, QDate, pyqtSignal, QUrl
from PyQt5.QtGui import QFont, QLinearGradient, QPainter, QBrush, QPen, QColor, QPixmap, QDesktopServices
from datetime import datetime

# Make it so the thumbnail widget sizes to the size of the thumbnail and not bigger than it
# Make it so the thumbnail scales to bigger sizes properly
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #8B0000")

        self.initUI()

        self.mod_thumbnail_label.clicked.connect(self.open_mod_url)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)


        self.create_mod_title_label()
        main_layout.addWidget(self.mod_title_label, 0, 0, 1, 4)

        self.create_mod_thumbnail_label()
        main_layout.addWidget(self.mod_thumbnail_label, 1, 0, 2, 2)

        self.create_mod_rating_label()
        main_layout.addWidget(self.mod_rating_label, 1, 2, 1, 2)

        self.create_mod_description_label()
        main_layout.addWidget(self.mod_description_label, 2, 2, 1, 2)

        self.create_no_button()
        main_layout.addWidget(self.no_button, 3, 0, 1, 2)

        self.create_yes_button()
        main_layout.addWidget(self.yes_button, 3, 2, 1, 2)

        self.create_maybe_button()
        main_layout.addWidget(self.maybe_button, 4, 0, 1, 4)


    def create_mod_title_label(self):
        """Creates a QLabel() for the mod title."""
        self.mod_title_label = QLabel("Ice Canyon")
        self.mod_title_label.setAlignment(Qt.AlignCenter)
        self.mod_title_label.setFont(QFont("Chewy", 20))
        self.mod_title_label.setStyleSheet("color: #F2F2E6; background-color: blue")

    def create_mod_thumbnail_label(self):
        """Creates a ClickableQLabel() to display the thumbnail for each mod."""
        self.thumbnail = QPixmap("ice_canyon.jpg")
        
        self.mod_thumbnail_label = ClickableQLabel()
        self.mod_thumbnail_label.setAlignment(Qt.AlignCenter)
        self.mod_thumbnail_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.thumbnail.scaled(self.mod_thumbnail_label.height(), self.mod_thumbnail_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.mod_thumbnail_label.setPixmap(self.thumbnail)
        self.mod_thumbnail_label.setStyleSheet("""
            ClickableQLabel:hover {
                background-color: rgba(0, 0, 0, 20)    
            }
        """)

    def create_mod_rating_label(self):
        """Creates a QLabel() for the rating for each mod."""
        rating_image = QPixmap("4-star.png")

        self.mod_rating_label = QLabel()
        self.mod_rating_label.setPixmap(rating_image)
        self.mod_rating_label.setStyleSheet("background-color: yellow")
        self.mod_rating_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def create_mod_description_label(self):
        """Creates a QLabel() for the description of each mod."""
        description = "\"The road is covered with snow, so the survivors will have to make their way through the icy canyon in search of salvation.\" Hello friends! Last December, I created the \"Ice Canyon\" map for the game Battle Grounds III. I decided to use it as a basis and cr..."

        self.mod_description_label = QLabel(description)
        self.mod_description_label.setWordWrap(True)
        self.mod_description_label.setFont(QFont("Chewy", 20, QFont.Medium))
        self.mod_description_label.setStyleSheet("background-color: grey")
        self.mod_description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def open_mod_url(self):
        """Opens the current mod's url in your browser."""
        QDesktopServices.openUrl(QUrl("https://steamcommunity.com/sharedfiles/filedetails/?id=3634176047&searchtext="))

    def resize_mod_thumbnail(self):
        self.thumbnail = QPixmap("ice_canyon.jpg")
        self.thumbnail = self.thumbnail.scaled(self.mod_thumbnail_label.width(), self.mod_thumbnail_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.mod_thumbnail_label.setPixmap(self.thumbnail)

    def create_no_button(self):
        self.no_button = QPushButton("No")
        self.no_button.setStyleSheet("background-color: red")
        self.no_button.setFont(QFont("Chewy", 15, QFont.Medium))
        self.no_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def create_yes_button(self):
        self.yes_button = QPushButton("Yes")
        self.yes_button.setStyleSheet("background-color: green")
        self.yes_button.setFont(QFont("Chewy", 15, QFont.Medium))
        self.yes_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def create_maybe_button(self):
        self.maybe_button = QPushButton("Maybe")
        self.maybe_button.setStyleSheet("background-color: pink")
        self.maybe_button.setFont(QFont("Chewy", 15, QFont.Medium))
        self.maybe_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resizeEvent(self, a0):
        self.resize_mod_thumbnail()
        return super().resizeEvent(a0)

class ClickableQLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)

    clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()
        return super().mousePressEvent(ev)
        

    # def create_mod_content_layout
        
        



        





app = QApplication([])
window = MainWindow()
window.show()
app.exec()
