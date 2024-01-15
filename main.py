import movie_addition
import inout
import game
import sys
from PySide6 import QtWidgets

if __name__ == "__main__":
    m = inout.MovieHandler
    app = QtWidgets.QApplication([])
    #widget = movie_addition.AdditionUI()
    widget = game.GameUI()
    sys.exit(app.exec())
