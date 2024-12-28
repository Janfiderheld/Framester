from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QRadioButton, QWidget
from PySide6.QtGui import QPixmap, QFont
import requests
from PySide6 import QtWidgets, QtCore

from model import MovieHandler, PlayerHandler

class GameUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.__max_height = QtWidgets.QApplication.screens()[0].size().height()
        self.__max_width = QtWidgets.QApplication.screens()[0].size().width()

        self.__movie_handler = MovieHandler()
        self.__player_handler = PlayerHandler()
        self.__curr_mov = self.__movie_handler.return_rand_movie()

        self.__btn_show_mov = QPushButton("Show Next Movie")
        self.__btn_show_mov.clicked.connect(self.show_new_mov)
        self.__btn_reveal = QPushButton("Reveal Answer")
        self.__btn_reveal.clicked.connect(self.reveal_info)
        self.__btn_exit = QPushButton("Exit")
        self.__btn_exit.clicked.connect(self.exit)

        self.__txt_res = QLabel("")
        self.__txt_res.setFont(QFont("Arial", 20))
        self.__txt_res.setWordWrap(True)  # Wrap long text
        self.__txt_res.setAlignment(QtCore.Qt.AlignCenter)  # Center-align text

        self.__txt_player = QLabel(f"{str(self.__player_handler.return_current_player())}")
        self.__txt_player.setFont(QFont("Arial", 24))

        self.__lbl_img = QLabel(self)
        self.__pix_img = QPixmap()

        self.layout_top = QVBoxLayout(self)
        self.layout_top.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout_time = self.visualise_timeline()

        self.update_layout(False, True)
        self.showFullScreen()

    def update_layout(self, show_btn: bool, rev_btn: bool):
        self.clear_layout(self.layout_top)
        self.clear_layout(self.layout_time)

        self.__btn_show_mov.setVisible(show_btn)
        self.__btn_reveal.setVisible(rev_btn)

        self.__txt_player = QLabel(f"{str(self.__player_handler.return_current_player())}")
        self.__txt_player.setFont(QFont("Arial", 24))
        self.get_img_from_url(self.__curr_mov.get_img())
        self.layout_time = self.visualise_timeline()

        self.layout_top.addWidget(self.__txt_player)
        self.layout_top.addLayout(self.layout_time)
        self.layout_top.addWidget(self.__lbl_img)
        self.layout_top.addWidget(self.__txt_res)
        self.layout_top.addWidget(self.__btn_show_mov)
        self.layout_top.addWidget(self.__btn_reveal)
        self.layout_top.addWidget(self.__btn_exit)

    @staticmethod
    def clear_layout(layout: QVBoxLayout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

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

    def visualise_timeline(self) -> QHBoxLayout:
        p = self.__player_handler.return_current_player()
        box = QHBoxLayout(self)
        rb0 = QRadioButton("", self)
        box.addWidget(rb0)

        for m in p.get_timeline():
            lbl = QLabel(f"{m.get_year()}")
            rb = QRadioButton("", self)
            box.addWidget(lbl)
            box.addWidget(rb)

        return box

    @QtCore.Slot()
    def show_new_mov(self):
        self.__txt_res.setText("")
        self.__curr_mov = self.__movie_handler.return_rand_movie()
        self.__player_handler.goto_next_player()
        self.update_layout(False, True)

    @QtCore.Slot()
    def reveal_info(self):
        rbs = [self.layout_time.itemAt(i).widget() for i in range(self.layout_time.count()) if isinstance(self.layout_time.itemAt(i).widget(), QRadioButton)]
        c_check = 0
        c_all = 0
        idx = 0
        for rb in rbs:
            if rb.isChecked():
                idx = c_all
                c_check += 1
            c_all += 1
        if c_check != 1:
            return

        p = self.__player_handler.return_current_player()
        if p.check_correct_pos_in_timeline(self.__curr_mov, idx):
            self.__txt_res.setText(f"Correct! {str(self.__curr_mov)}")
            p.add_to_timeline(self.__curr_mov, idx)
        else:
            self.__txt_res.setText(f"Incorrect! {str(self.__curr_mov)}")

        if p.check_win():
            self.__txt_res.setText(f"{self.__txt_res.text()}\nPlayer {p.get_name()} has won!")
            self.update_layout(False, False)
        else:
            self.update_layout(True, False)

    @QtCore.Slot()
    def exit(self):
        self.close()
