"""
Created by: Zasko B.
GUI implementation of the app
"""

import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QListWidgetItem, QDialog
from PyQt5.QtGui import QPixmap

import Data


class Main(QMainWindow):
    """ Main GUI class """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("gui.ui", self)
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("Future Library")

        self.ui.notFound.hide()

        self.ui.showMenu.clicked.connect(self.menu_show)
        self.ui.hideMenu.clicked.connect(self.menu_hide)
        self.ui.homeButton.clicked.connect(self.home)
        self.ui.libraryButton.clicked.connect(self.library)
        self.ui.recommendationsButton.clicked.connect(self.recommendations)
        self.ui.randomButton.clicked.connect(self.get_random_game)
        self.ui.aboutButton.clicked.connect(self.about)
        self.ui.searchButton.clicked.connect(self.search)
        self.ui.page.textEdited.connect(self.page_enter)
        self.ui.gamesList.itemClicked.connect(self.game_chosen)
        self.ui.changePageButton.clicked.connect(self.page_change)
        self.ui.firstPage.clicked.connect(self.first)
        self.ui.prevPage.clicked.connect(self.previous)
        self.ui.nextPage.clicked.connect(self.next)
        self.ui.lastPage.clicked.connect(self.last)
        self.ui.gameLibraryState.linkActivated.connect(self.library_state_change)
        self.ui.gamePlatforms.linkActivated.connect(self.platforms)
        self.ui.gameGenres.linkActivated.connect(self.genres)
        self.ui.gameThemes.linkActivated.connect(self.themes)
        self.ui.gameDevelopers.linkActivated.connect(self.developers)
        self.ui.gamePublishers.linkActivated.connect(self.publishers)
        self.ui.gameClose.clicked.connect(self.close_game)

        self.items_per_page = 14  # Random value, can be received from user; shows amount of items per page
        self.current_work_state = "home"  # Init value; shows current working mod of app
        self.temp_window_name = "Future Library"  # Init value; stores window name depending on current working mod
        if Data.NUMBER_OF_GAMES == 0:
            self.home_pages = 1  # Init value; shows number of pages for game tab
        else:
            self.home_pages = (Data.NUMBER_OF_GAMES // self.items_per_page)
            if Data.NUMBER_OF_GAMES % self.items_per_page != 0:
                self.home_pages += 1
        self.temp_library_flag = None  # Placeholder value; used for 'knowing' if game library state was changed or not
        self.library_pages = 1  # Placeholder value; shows number of pages for library tab
        self.characteristic_pages = 1  # Placeholder value; shows number of pages for chosen characteristic tab
        self.characteristic_text = ""  # Placeholder value; shows value of chosen characteristic
        self.characteristic = ""  # Placeholder value; shows chosen characteristic
        self.current_page = 1  # Init value; shows which page is currently displayed
        self.current_game = None  # Placeholder value; stores currently displayed game
        self.current_games = []  # Placeholder value; stores currently displayed games in games tab

        self.home()  # Init state of app

    def menu_show(self):
        """ Shows menu """
        self.ui.sidePanel.show()
        self.ui.mainPanel.setEnabled(False)
        self.ui.topPanel.setEnabled(False)
        self.ui.showMenu.hide()

    def menu_hide(self):
        """ Hides menu """
        self.ui.sidePanel.hide()
        self.ui.mainPanel.setEnabled(True)
        self.ui.topPanel.setEnabled(True)
        self.ui.showMenu.show()

    def first(self):
        """ Changes page to first """
        self.current_page = 1
        self.change_page_by_buttons()

    def previous(self):
        """ Changes page to previous """
        self.current_page -= 1
        self.change_page_by_buttons()

    def next(self):
        """ Changes page to next """
        self.current_page += 1
        self.change_page_by_buttons()

    def last(self):
        """ Changes page to last """
        if self.current_work_state == "home":
            self.current_page = self.home_pages
        elif self.current_work_state == "library":
            self.current_page = self.library_pages
        elif self.current_work_state == "characteristic":
            self.current_page = self.characteristic_pages
        self.change_page_by_buttons()

    def change_page_by_buttons(self):
        """ End function for navigation buttons """
        self.ui.page.setText(str(self.current_page))
        self.ui.page.clearFocus()
        self.games_list()

    def page_enter(self, text):
        """ Controls page number input """
        try:
            page = int(text)
            if (self.current_work_state == "home" and page > self.home_pages) or \
                    (self.current_work_state == "library" and page > self.library_pages) or \
                    (self.current_work_state == "characteristic" and page > self.characteristic_pages):
                raise ValueError
        except ValueError:
            self.ui.page.setText(text[:-1])

    def page_change(self):
        """ Changes the page """
        text = self.ui.page.text()
        if text == "":
            self.ui.page.setText("1")
            self.current_page = 1
        else:
            self.current_page = int(text)
        self.ui.page.clearFocus()
        self.games_list()

    def home(self):
        """ Home tab function """
        if self.current_work_state == "home":
            self.games_list()
        else:
            self.current_work_state = "home"
            self.temp_window_name = "Future Library"
            self.current_page = 1
            self.ui.page.setText("1")
            self.games_list()
        self.setWindowTitle(self.temp_window_name)

    def library(self):
        """ Library tab function """
        if self.current_work_state == "library":
            self.games_list()
        else:
            self.current_work_state = "library"
            self.temp_window_name = "Future Library - Library"
            self.current_page = 1
            self.ui.page.setText("1")
            Data.library_len()
            if Data.LEN_OF_LIBRARY == 0:
                self.library_pages = 1
            else:
                self.library_pages = (Data.LEN_OF_LIBRARY // self.items_per_page)
                if Data.LEN_OF_LIBRARY % self.items_per_page != 0:
                    self.library_pages += 1
            self.games_list()
        self.setWindowTitle(self.temp_window_name)

    def recommendations(self):
        """
        Recommendations tab function
        """
        if self.current_work_state == "recommendations":
            self.games_list()
        else:
            self.current_work_state = "recommendations"
            self.temp_window_name = "Future Library - Recommendations"
            self.current_page = 1
            self.ui.page.setText("1")
            self.games_list()
        self.setWindowTitle(self.temp_window_name)

    def games_list(self):
        """ Generates games list for current page and operates state of navigation buttons"""
        self.ui.gamesList.clear()
        if self.current_work_state == "home":
            max_limit = self.home_pages
            self.current_games = Data.home_page(self.current_page, self.items_per_page)
        elif self.current_work_state == "library":
            max_limit = self.library_pages
            self.current_games = Data.library_page(self.current_page, self.items_per_page)
        elif self.current_work_state == "recommendations":
            max_limit = 1
            self.current_games = Data.analyze_library()
        elif self.current_work_state == "characteristic":
            max_limit = self.characteristic_pages
            self.current_games = Data.chosen_characteristic(self.characteristic_text, self.characteristic,
                                                            self.current_page, self.items_per_page)
        else:
            max_limit = 0
            self.current_games = []
        if self.current_page == 1:
            self.ui.firstPage.setEnabled(False)
            self.ui.prevPage.setEnabled(False)
        else:
            self.ui.firstPage.setEnabled(True)
            self.ui.prevPage.setEnabled(True)
        if self.current_page == max_limit:
            self.ui.nextPage.setEnabled(False)
            self.ui.lastPage.setEnabled(False)
        else:
            self.ui.nextPage.setEnabled(True)
            self.ui.lastPage.setEnabled(True)
        if max_limit == 1:
            self.ui.page.setEnabled(False)
            self.ui.changePageButton.setEnabled(False)
        else:
            self.ui.page.setEnabled(True)
            self.ui.changePageButton.setEnabled(True)
        self.menu_hide()
        self.ui.gamePanel.hide()
        self.ui.gamesListPanel.show()
        for i in range(len(self.current_games)):
            game = self.current_games[i]
            if self.current_work_state == "library":
                string = game.name + "\nRelease date: " + str(game.release_date) + \
                         "   Your rating: " + str(game.get_rating()) + "/10"
                item = QListWidgetItem(string)
                item.setData(737, game)
                self.ui.gamesList.addItem(item)
            else:
                string = game.name + "\nRelease date: " + str(game.release_date)
                item = QListWidgetItem(string)
                item.setData(737, game)
                self.ui.gamesList.addItem(item)

    def game_chosen(self, item):
        """ Detects which game was chosen in game list """
        self.current_game = item.data(737)
        self.set_game_info(self.current_game)

    @staticmethod
    def about():
        """ About message """
        about_message = QMessageBox()
        about_message.setWindowTitle("About")
        about_message.setText("All data provided by GiantBomb.com")
        about_message.addButton('OK', QMessageBox.AcceptRole)
        about_message.exec_()

    def get_random_game(self):
        """ Gets random game """
        self.menu_hide()
        game = Data.random_game()
        self.current_game = game
        self.set_game_info(self.current_game)

    def search(self):
        """ Gets game by name """
        game = Data.game_by_name(self.ui.searchField.text())
        if game is not None:
            self.current_game = game
            self.set_game_info(self.current_game)
        else:
            timer = QTimer(self)
            timer.setSingleShot(True)
            self.ui.notFound.show()
            timer.timeout.connect(self.ui.notFound.hide)
            timer.start(3000)

    def set_game_info(self, game):
        """ Fills game tab """
        self.temp_library_flag = False
        self.ui.gameName.setText(game.name)
        self.ui.gameDesc.setText(game.desc)
        self.ui.gamePicture.setPixmap(QPixmap("res/NoImage.jpg"))
        self.ui.gameDate.setText("Release date: " + str(game.release_date))
        if game.library_state():
            self.ui.gameLibraryState.setText("<a href='#remove'>Remove from library</a>")
        else:
            self.ui.gameLibraryState.setText("<a href='#add'>Add to library</a>")
        self.ui.gamePlatforms.setText(Data.Game.generate_text("Platforms", game.platforms))
        self.ui.gameGenres.setText(Data.Game.generate_text("Genres", game.genres))
        self.ui.gameThemes.setText(Data.Game.generate_text("Themes", game.themes))
        self.ui.gameDevelopers.setText(Data.Game.generate_text("Developers", game.developers))
        self.ui.gamePublishers.setText(Data.Game.generate_text("Publishers", game.publishers))
        self.ui.gamesListPanel.hide()
        self.ui.gamePanel.show()
        self.setWindowTitle("Future Library - Game: {:100}".format(game.name))

    def library_state_change(self, link):
        """ Adds game to the library or removes it """
        if link == "#add":
            add_message = AddDialog()
            if add_message.exec_():
                self.current_game.add_to_library(add_message.value)
                self.set_game_info(self.current_game)
                if self.current_work_state in ["library", "recommendations"]:
                    self.temp_library_flag = True
        elif link == "#remove":
            self.current_game.remove_from_library()
            self.set_game_info(self.current_game)
            if self.current_work_state in ["library", "recommendations"]:
                self.temp_library_flag = True

    def platforms(self, link):
        """ Platform query """
        self.current_work_state = "characteristic"
        self.characteristic = "platform"
        self.characteristic_text = link
        self.characteristic_init()

    def genres(self, link):
        """ Genre query"""
        self.current_work_state = "characteristic"
        self.characteristic = "genre"
        self.characteristic_text = link
        self.characteristic_init()

    def themes(self, link):
        """ Theme query """
        self.current_work_state = "characteristic"
        self.characteristic = "theme"
        self.characteristic_text = link
        self.characteristic_init()

    def developers(self, link):
        """ Developer query """
        self.current_work_state = "characteristic"
        self.characteristic = "developer"
        self.characteristic_text = link
        self.characteristic_init()

    def publishers(self, link):
        """ Publisher query """
        self.current_work_state = "characteristic"
        self.characteristic = "publisher"
        self.characteristic_text = link
        self.characteristic_init()

    def characteristic_init(self):
        """ End function for querying games by chosen characteristic"""
        self.characteristic_pages = Data.chosen_characteristic(self.characteristic_text, self.characteristic)
        temp = self.characteristic_pages
        self.characteristic_pages = (self.characteristic_pages // self.items_per_page)
        if temp % self.items_per_page != 0:
            self.characteristic_pages += 1
        self.current_page = 1
        self.ui.page.setText("1")
        self.games_list()
        self.temp_window_name = "{} - {}: {:100}".format("Future Library", self.characteristic.capitalize(),
                                                         self.characteristic_text.replace("_", " "))
        self.setWindowTitle(self.temp_window_name)

    def close_game(self):
        """ Closes game tab """
        self.ui.gamePanel.hide()
        if self.temp_library_flag:
            if self.current_work_state == "library":
                self.current_work_state = "temp"
                self.library()
            elif self.current_work_state == "recommendations":
                self.current_work_state = "temp"
                self.recommendations()
        else:
            self.ui.gamesListPanel.show()
        self.setWindowTitle(self.temp_window_name)


class AddDialog(QDialog):
    """ Dialog for adding game to library """
    def __init__(self):
        flags = Qt.WindowCloseButtonHint
        QDialog.__init__(self, flags=flags)
        self.ui = uic.loadUi("dialogTrue.ui", self)
        self.ui.confirm.clicked.connect(self.confirm_func)
        self.setWindowTitle("Rate game")
        self.setFixedSize(self.width(), self.height())
        # self.ui.without.linkActivated.connect(self.without_func)
        self.value = ""

    def confirm_func(self):
        self.value = self.ui.rating.value()
        self.accept()

    # def without_func(self, link):
    #     self.value = "without"
    #     self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
