import sys
from PySide6 import QtWidgets
from movie_addition.addition_ui import AdditionUI


def add_new_movies():
    app = QtWidgets.QApplication([])

    widget = AdditionUI()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
