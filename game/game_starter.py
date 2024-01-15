import sys
from PySide6 import QtWidgets
from game.game_ui import GameUI


def start_game():
    app = QtWidgets.QApplication([])

    widget = GameUI()
    widget.show()

    sys.exit(app.exec())
