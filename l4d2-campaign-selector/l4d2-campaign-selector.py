from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QSizePolicy, QLabel, QGridLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QUrl, QSize, QTimer
from PyQt5.QtGui import QFont, QPixmap, QDesktopServices
from mod_display_logic import ModDisplayLogic
from left_4_dead_2_scraper.l4d2_scraper import Scraper

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
        """Initializes the user interface by creating a layout and widgets."""
        # Create main layout.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)

        # Create all widgets.
        self.create_mod_title_label(main_layout=main_layout)
        self.create_mod_thumbnail_label(main_layout=main_layout)
        self.create_mod_rating_label(main_layout=main_layout)
        self.create_mod_description_label(main_layout=main_layout)
        self.create_buttons(main_layout=main_layout)
        self.create_mods_left_label(main_layout=main_layout)
    
    def updateUI(self):
        """Updates the user interface with new information for every mod."""
        self.mod_display_logic.update_current_mod()
        
        if self.mod_display_logic.current_mod == "placeholder":
            current_mod_details = self.set_placeholders()
        else:
            current_mod_details = self.mod_display_logic.get_current_mod_details()
            
        mod_title = current_mod_details[0]
        mod_thumbnail_url = current_mod_details[1]
        mod_rating = current_mod_details[2]
        mod_url = current_mod_details[3]
        mod_description = current_mod_details[4]

        # Updates the mod's name.
        self.mod_title_label.setText(mod_title)

        # Updates the total number and number of mods left.
        total_number_of_mods = self.mod_display_logic.get_total_number_of_mods()
        number_of_mods_left = self.mod_display_logic.get_number_of_mods_left()
        self.mods_left_label.setText(f"Total Mods- {total_number_of_mods}   Mods Left- {number_of_mods_left}")

        # Updates the mod's thumbnail image.
        mod_thumbnail = QPixmap()
        mod_thumbnail.loadFromData(self.l4d2_scraper.get_mod_thumbnail_image_in_bytes(mod_thumbnail_url))
        mod_thumbnail_size = QSize(int(self.mod_thumbnail_label.width() * 1), int(self.mod_thumbnail_label.height() * 1))
        mod_thumbnail = mod_thumbnail.scaled(mod_thumbnail_size, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.mod_thumbnail_label.setPixmap(mod_thumbnail)

        # Updates the mod's rating image.
        mod_rating_image = self.change_mod_rating_image(mod_rating)
        self.mod_rating_label.setPixmap(mod_rating_image)

        # Updates the mod's url.
        self.mod_url = mod_url

        # Updates the mod's description.
        self.mod_description_label.setText(mod_description)
    
    def set_window_properties(self):
        """Sets various properties of the application's window."""
        self.setWindowTitle("Left 4 Dead 2 Campaign Selector")
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #1E0000")
        self.setContentsMargins(100, 0, 100, 0)
        self.showMaximized()

    def create_mod_title_label(self, main_layout):
        """
        Creates the QLabel() widget that displays the name of the current mod.
        
        :param main_layout: The main layout that the entire application is based off of.
        """
        self.mod_title_label = QLabel()
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
        """
        Creates the ClickableQLabel() widget that displays the thumbnail image of the current mod.
        
        :param main_layout: The main layout that the entire application is based off of.
        """
        self.mod_thumbnail_label = ClickableQLabel()    # A class that inherits from QLabel() that allows it to be clicked.
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
 
        main_layout.addWidget(self.mod_thumbnail_label, 2, 0, 2, 1)

    def create_mod_rating_label(self, main_layout):
        """
        Creates the QLabel() widget that displays the rating image of the current mod.
        
        :param main_layout: The main layout that the entire application is based off of.
        """
        self.mod_rating_label = QLabel()
        self.mod_rating_label.setFixedSize(QSize(848, 180))
        self.mod_rating_label.setAlignment(Qt.AlignCenter)
        self.mod_rating_label.setStyleSheet("""
            background-color: #2A2A2A; 
            border: 2px solid #4A1A1A;
            padding-right: 15px; 
            padding-left: 15px; 
            padding-top: 15px; 
            padding-bottom: 15px
        """)

        main_layout.addWidget(self.mod_rating_label, 2, 1, 1, 1)
        main_layout.setRowStretch(1, 1)

    def create_mod_description_label(self, main_layout):
        """
        Creates the QLabel() widget that displays the description of the current mod.
        
        :param main_layout: The main layout that the entire application is based off of.
        """
        self.mod_description_label = QLabel()
        self.mod_description_label.setFixedSize(848, 562) # 600
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
        main_layout.addWidget(self.mod_description_label, 3, 1, 1, 1)

    def create_buttons(self, main_layout):
        """
        Creates the QPushButton() widgets that allow the user to select no, yes, or maybe to a mod.
        
        :param main_layout: The main layout that the entire application is based off of.
        """
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
        main_layout.addWidget(self.no_button, 4, 0, 1, 1)

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
        main_layout.addWidget(self.yes_button, 4, 1, 1, 1)
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
        main_layout.addWidget(self.maybe_button, 5, 0, 1, 2)
        main_layout.setRowStretch(4, 1)

    def create_mods_left_label(self, main_layout):
        """
        Creates the QLabel() widget that displays the total number of mods and number of mods left.
        
        :param main_layout: The main layout that the entire application is based off of.
        """
        self.mods_left_label = QLabel()
        self.mods_left_label.setFont(QFont("Chewy", 25))
        self.mods_left_label.setAlignment(Qt.AlignCenter)
        self.mods_left_label.setStyleSheet("""
            color: #F2F2E6; 
            background-color: #2A2A2A; 
            border: 2px solid #4A1A1A
        """)

        main_layout.setRowStretch(5, 1)
        main_layout.addWidget(self.mods_left_label, 1, 0, 1, 2)

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
        elif "placeholder" in mod_rating_image_url: # Changes the image to placeholder when there are no more mods left.
            image = "l4d2_campaign_selector/placeholder_images/l4d2_b4b_player_count_comparison.png"

        mod_rating_image.load(image)
        mod_rating_image = mod_rating_image.scaled(self.mod_thumbnail_label.width(), self.mod_thumbnail_label.height(), Qt.KeepAspectRatio, Qt.FastTransformation)
        return mod_rating_image

    def button_pressed(self):
        """
        Is called whenever a button is clicked.
        
        Then, it calls a method from ModDisplayLogic to add the current mod 
        to a json file corresponding with the button clicked.
        """
        match self.sender():
            case self.yes_button:
                self.mod_display_logic.yes_button_clicked()
            case self.no_button:
                self.mod_display_logic.no_button_clicked()
            case self.maybe_button:
                self.mod_display_logic.maybe_button_clicked()
        self.updateUI()

    def open_mod_url(self):
        """Opens the current mod's url in the user's browser."""
        QDesktopServices.openUrl(QUrl(self.mod_url))

    def set_placeholders(self):
        mod_title = "There are no more mods left."
        mod_thumbnail_url = "https://imgs.search.brave.com/VhknJ3rE0VcgNcfyT4_MIF1SkBGaUbN86CBW8NHomA8/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pLnJl/ZGQuaXQvbWFpYmQ3/ZzV2ZWhmMS5wbmc"
        mod_rating = "placeholder"
        mod_url = "https://www.reddit.com/r/l4d2/comments/1mj6h42/when_you_know_theres_a_jockey_in_the_map_but_you/"
        mod_description = """
But You Can't Prove It, also known as James Doakes Reaction Images, 
refers to a series of image caption memes using reaction images of 
Dexter character James Doakes (played by actor Erik King) with 
determined looks on his face, including an image of him driving a 
car and an image of him holding a drink in a bar. The memes feature 
captions about knowing that someone is hiding a secret from you, 
but you can't prove it, a reference to Doakes, who believes Dexter 
Morgan is a serial killer but is unable to prove it. The format 
was popularized online throughout 2025 on sites like TikTok and 
X / Twitter, first appearing online as early as September 2024 on 
Reddit.
        """
        mod_description = mod_description.replace("\n", "")

        self.no_button.setDisabled(True)
        self.yes_button.setDisabled(True)
        self.maybe_button.setDisabled(True)

        return mod_title, mod_thumbnail_url, mod_rating, mod_url, mod_description

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
    """A class that inherits from QLabel() that allows it to be clicked."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)

    clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        """Called when a ClickableQLabel() is clicked."""
        self.clicked.emit()
        return super().mousePressEvent(ev)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
