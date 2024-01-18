from PySide6 import QtWidgets, QtCore

import ui
from data import write_top250_to_csv, add_movies_from_top250
from model import PlayerHandler, Player


class StartupUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.__game_window = QtWidgets.QWidget()
        self.__add_window = QtWidgets.QWidget()
        self.__player_handler = PlayerHandler()

        self.__btn_start = QtWidgets.QPushButton("Start Game")
        self.__btn_start.clicked.connect(self.start_game)
        self.__btn_add_movie = QtWidgets.QPushButton("Add new Movie")
        self.__btn_add_movie.clicked.connect(self.add_movie)
        self.__btn_import_250 = QtWidgets.QPushButton("Import IMDB Top 250 Movies")
        self.__btn_import_250.clicked.connect(self.import_top250)

        self.__btn_add_player = QtWidgets.QPushButton("+")
        self.__btn_add_player.clicked.connect(self.add_player)
        self.__btn_rem_player = QtWidgets.QPushButton("-")
        self.__btn_rem_player.clicked.connect(self.rem_player)

        self.__player_list = QtWidgets.QListWidget()
        self.__txt_header = QtWidgets.QLabel("Current Players:")
        self.__ed_player_name = QtWidgets.QLineEdit()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout_btn = QtWidgets.QHBoxLayout(self)

        self.layout_btn.addWidget(self.__ed_player_name)
        self.layout_btn.addWidget(self.__btn_add_player)
        self.layout_btn.addWidget(self.__btn_rem_player)

        self.layout.addWidget(self.__txt_header)
        self.layout.addWidget(self.__player_list)
        self.layout.addLayout(self.layout_btn)
        self.layout.addWidget(self.__btn_start)
        self.layout.addWidget(self.__btn_add_movie)
        self.layout.addWidget(self.__btn_import_250)

        self.resize(800, 600)
        self.show()

    @QtCore.Slot()
    def start_game(self):
        if self.__player_list.count() == 0:
            print("No Players")
            return

        for idx in range(self.__player_list.count()):
            i = self.__player_list.item(idx)
            p = Player(i.text())
            self.__player_handler.add_new_player(p)

        self.__game_window = ui.GameUI()
        self.close()

    @QtCore.Slot()
    def add_movie(self):
        self.__add_window = ui.AdditionUI()
        self.close()

    @QtCore.Slot()
    def import_top250(self):
        write_top250_to_csv()
        add_movies_from_top250()
        print("Import of Top 250 from IMDB successful")

    @QtCore.Slot()
    def add_player(self):
        if not self.__ed_player_name.text():
            return
        self.__player_list.addItem(self.__ed_player_name.text())
        self.__ed_player_name.setText("")

    @QtCore.Slot()
    def rem_player(self):
        selected_item = self.__player_list.currentItem()
        if selected_item:
            index = self.__player_list.row(selected_item)
            self.__player_list.takeItem(index)
