from PySide6 import QtWidgets, QtCore


class AdditionUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.__btn_add = QtWidgets.QPushButton("Add Movie")

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

        self.__btn_add.clicked.connect(self.add_movie)

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
        if not self.__ed_img.text():
            print("Image URL is empty")
            return

        print(f"Add {self.__ed_name.text()} ({self.__ed_year.text()}) from {self.__ed_direct.text()} with img: {self.__ed_img.text()}")
        # add movie info to db
