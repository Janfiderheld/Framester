import sys

from PySide6 import QtWidgets

import ui
from model import MovieHandler

if __name__ == "__main__":
    m = MovieHandler
    app = QtWidgets.QApplication([])
    #widget = ui.AdditionUI()
    widget = ui.GameUI()
    sys.exit(app.exec())
