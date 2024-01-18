from PySide6 import QtWidgets, QtCore

from model import Movie, MovieHandler


class AdditionUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.__movie_handler = MovieHandler()

        self.__btn_add = QtWidgets.QPushButton("Add Movie")
        self.__btn_save = QtWidgets.QPushButton("Save additions")

        self.__txt_name = QtWidgets.QLabel("Name:")
        self.__txt_direct = QtWidgets.QLabel("Director:")
        self.__txt_year = QtWidgets.QLabel("Year:")
        self.__txt_img = QtWidgets.QLabel("Image URL:")

        self.__ed_name = QtWidgets.QLineEdit("")
        self.__ed_direct = QtWidgets.QLineEdit("")
        self.__ed_year = QtWidgets.QLineEdit("")
        self.__ed_img = QtWidgets.QLineEdit("")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.__txt_name)
        self.layout.addWidget(self.__ed_name)
        self.layout.addWidget(self.__txt_direct)
        self.layout.addWidget(self.__ed_direct)
        self.layout.addWidget(self.__txt_year)
        self.layout.addWidget(self.__ed_year)
        self.layout.addWidget(self.__txt_img)
        self.layout.addWidget(self.__ed_img)
        self.layout.addWidget(self.__btn_add)
        self.layout.addWidget(self.__btn_save)

        self.__btn_add.clicked.connect(self.add_movie)
        self.__btn_save.clicked.connect(self.save_movies)

        self.resize(800, 600)
        self.show()

    @QtCore.Slot()
    def add_movie(self):
        if not self.__ed_name.text():
            print("Name is empty")
            return
        if not self.__ed_direct.text():
            print("Director is empty")
            return
        if not self.__ed_year.text():
            print("Year is empty")
            return
        if not self.__ed_year.text().isdigit():
            print("Year is not a number")
            return
        if not self.__ed_img.text():
            print("Image URL is empty")
            return

        m = Movie(self.__ed_name.text(), self.__ed_direct.text(), int(self.__ed_year.text()), self.__ed_img.text())
        self.__movie_handler.add_new_movie(m)

    @QtCore.Slot()
    def save_movies(self):
        self.__movie_handler.export_movies()
