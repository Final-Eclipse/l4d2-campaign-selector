from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QSizePolicy, QVBoxLayout, QLabel, 
                             QHBoxLayout, QGraphicsDropShadowEffect, QGraphicsEffect, QTextEdit,
                             QGridLayout, QPushButton)
from PyQt5.QtCore import Qt, QPropertyAnimation, QPointF, QTimer, QDateTime, QDate, pyqtSignal, QUrl, QSize, QTimer
from PyQt5.QtGui import QFont, QLinearGradient, QPainter, QBrush, QPen, QColor, QPixmap, QDesktopServices
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from datetime import datetime
from mod_display_logic import ModDisplayLogic
from left_4_dead_2_scraper.l4d2_scraper import Scraper

# Add a container widget to the thumbnail so that the mod url only open when you click directly on the image and not the borders of the widget

# Add functionality for the maybe button to add it to the maybe text file

# Handle what happens when there are no mods left, go to all mods that were in maybe text file and loop through those.  
# Make sure to delete them from the maybe text file or rewrite the file with that mod gone
# Make sure to add the mod to liked or disliked text file
# Then, after all mods have been exhausted put a placeholder thumbnail, title, rating, and description

# Either download all possible rating images (0, 1, 2, 3, 4, 5 stars) and display them based on the 
# mod's rating url or use requests to get the content of the rating image url and display it (requests 
# is currently being used, most likely slower than storing images because it has to make requests)

# Instead of writing the name of the mod to the liked and disliked files,
# Create a dictionary and write in json instead

# Add a "Mods Left" widget to the GUI
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.l4d2_scraper = Scraper()
        self.mod_display_logic = ModDisplayLogic()

        self.set_window_properties()
        self.initUI() 
        self.updateUI()

        self.mod_thumbnail_label.clicked.connect(self.open_mod_url)
        
        self.yes_button.clicked.connect(self.button_pressed)
        self.no_button.clicked.connect(self.button_pressed)
        self.maybe_button.clicked.connect(self.button_pressed)
    
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
    
    def updateUI(self):
        """Updates the User Interface with new information for every mod."""
        self.mod_display_logic.update_current_mod()
        current_mod_details = self.mod_display_logic.get_current_mod_details()

        self.mod_title_label.setText(current_mod_details[0])

        mod_thumbnail = QPixmap()
        mod_thumbnail.loadFromData(self.l4d2_scraper.get_mod_thumbnail_image_in_bytes(current_mod_details[1]))
        mod_thumbnail_size = QSize(int(self.mod_thumbnail_label.width() * 0.85), int(self.mod_thumbnail_label.height() * 0.85))
        mod_thumbnail = mod_thumbnail.scaled(mod_thumbnail_size, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.mod_thumbnail_label.setPixmap(mod_thumbnail)

        mod_rating_image = self.change_mod_rating_image(current_mod_details[2])
        self.mod_rating_label.setPixmap(mod_rating_image)

        self.mod_url = current_mod_details[3]
        self.mod_description_label.setText(current_mod_details[4])
    
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
        # mod_rating_image = QPixmap()
        # mod_rating_image = mod_rating_image.scaled(self.mod_thumbnail_label.width(), self.mod_thumbnail_label.height(), Qt.KeepAspectRatio, Qt.FastTransformation)

        self.mod_rating_label = QLabel()
        self.mod_rating_label.setFixedSize(QSize(848, 180))
        # self.mod_rating_label.setPixmap(mod_rating_image)
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
        self.mod_description_label = QLabel()
        self.mod_description_label.setFixedSize(848, 600)
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
        """Creates the no, yes, and maybe buttons."""
        self.no_button = QPushButton("No")
        self.no_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.no_button.setFont(QFont("Chewy", 45))
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
        self.yes_button.setFont(QFont("Chewy", 45))
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
        self.maybe_button.setFont(QFont("Chewy", 45))
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

    def get_mod_rating_pixmaps(self):
        """Returns a dictionary of urls for each possible mod rating image."""
        mod_rating_images = {
            "not-yet.png": "l4d2_campaign_selector/mod_star_ratings/not-yet.png",
            "1-star.png": "l4d2_campaign_selector/mod_star_ratings/1-star.png",
            "2-star.png": "l4d2_campaign_selector/mod_star_ratings/2-star.png",
            "3-star.png": "l4d2_campaign_selector/mod_star_ratings/3-star.png",
            "4-star.png": "l4d2_campaign_selector/mod_star_ratings/4-star.png",
            "5-star.png": "l4d2_campaign_selector/mod_star_ratings/5-star.png"
        }

        return mod_rating_images
    
    def change_mod_rating_image(self, mod_rating_image_url):
        """
        Checks the current mod's url for the rating and changes the image on the GUI to it.
        
        :param mod_rating_image_url: The url to the mod's rating image.
        """
        mod_rating_image = QPixmap()
        
        all_mod_rating_images = self.get_mod_rating_pixmaps()

        if "not-yet.png" in mod_rating_image_url:
            image = all_mod_rating_images["not-yet.png"]
        elif "1-star.png" in mod_rating_image_url:
            image = all_mod_rating_images["1-star.png"]
        elif "2-star.png" in mod_rating_image_url:
            image = all_mod_rating_images["2-star.png"]
        elif "3-star.png" in mod_rating_image_url:
            image = all_mod_rating_images["3-star.png"]
        elif "4-star.png" in mod_rating_image_url:
            image = all_mod_rating_images["4-star.png"]
        elif "5-star.png" in mod_rating_image_url:
            image = all_mod_rating_images["5-star.png"]

        mod_rating_image.load(image)
        mod_rating_image = mod_rating_image.scaled(self.mod_thumbnail_label.width(), self.mod_thumbnail_label.height(), Qt.KeepAspectRatio, Qt.FastTransformation)
        return mod_rating_image

    def button_pressed(self):
        """Is called as a slot when a clicked signal is sent from any of the three buttons."""
        match self.sender():
            case self.yes_button:
                self.mod_display_logic.add_current_mod_to_liked()
            case self.no_button:
                self.mod_display_logic.add_current_mod_to_disliked()
            # case self.maybe_button:
            #     self.mod_display_logic.add_current_mod_maybe()
        self.updateUI()

    def open_mod_url(self):
        """Opens the current mod's url in your browser."""
        QDesktopServices.openUrl(QUrl(self.mod_url))

    def resize_mod_thumbnail(self):
        """Changes the size of the mod's thumbnail when resizing the window."""
        # Prevents AttributeError when starting application because this method is called 
        # from self.resizeEvent() before self.mod_thumbnail_label is created in self.initUI()
        if hasattr(self, "mod_thumbnail_label") == True:    
            self.updateUI()

    def resizeEvent(self, a0):
        """
        At application start, is called once.
        After application start, is only called the window is resized.
        """
        # Resizes widgets after 1 second of resizing the window to prevent lag from resizing all widgets instantly when window size changes
        QTimer.singleShot(1000, self.resize_mod_thumbnail)  

        return super().resizeEvent(a0)

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