import requests
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QPixmap

from model import MovieHandler


class GameUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.__max_height = QtWidgets.QApplication.screens()[0].size().height()
        self.__max_width = QtWidgets.QApplication.screens()[0].size().width()

        self.__movie_handler = MovieHandler()
        self.__curr_mov = None
        self.__curr_mov = self.__movie_handler.return_rand_movie()

        self.__btn_show_mov = QtWidgets.QPushButton("Show New Movie")
        self.__btn_reveal = QtWidgets.QPushButton("Reveal Info")
        self.__btn_exit = QtWidgets.QPushButton("Exit")

        self.__txt_res = QtWidgets.QLabel("")
        self.__txt_res.setStyleSheet("""font:'SF Pro Display';
                                        font-size:20pt;
                                        font-weight:750;""")

        self.__lbl_img = QtWidgets.QLabel(self)
        self.__pix_img = QPixmap()
        self.get_img_from_url(self.__curr_mov.get_img())

        self.layout_top = QtWidgets.QVBoxLayout(self)
        self.layout_top.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout_btns = QtWidgets.QHBoxLayout(self)

        self.layout_btns.addWidget(self.__btn_show_mov)
        self.layout_btns.addWidget(self.__btn_reveal)
        self.layout_btns.addWidget(self.__btn_exit)

        self.layout_top.addWidget(self.__lbl_img)
        self.layout_top.addWidget(self.__txt_res)
        self.layout_top.addLayout(self.layout_btns)

        self.__btn_show_mov.clicked.connect(self.show_new_mov)
        self.__btn_reveal.clicked.connect(self.reveal_info)
        self.__btn_exit.clicked.connect(self.exit)

        self.showFullScreen()

    def get_img_from_url(self, img: str):
        req = requests.get(img)
        self.__pix_img.loadFromData(req.content)
        sizes = self.calc_img_size()
        self.__pix_img = self.__pix_img.scaled(sizes[0], sizes[1], QtCore.Qt.KeepAspectRatio)
        self.__lbl_img.setPixmap(self.__pix_img)

    def calc_img_size(self) -> (int, int):
        w = min(self.__max_width * 0.8, self.__pix_img.width())
        h = min(self.__max_height * 0.8, self.__pix_img.height())
        return w, h

    @QtCore.Slot()
    def show_new_mov(self):
        self.__txt_res.setText("")
        self.__curr_mov = self.__movie_handler.return_rand_movie()
        self.get_img_from_url(self.__curr_mov.get_img())

    @QtCore.Slot()
    def reveal_info(self):
        self.__txt_res.setText(str(self.__curr_mov))

    @QtCore.Slot()
    def exit(self):
        self.close()
