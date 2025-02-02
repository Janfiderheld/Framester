import sys

from PySide6 import QtWidgets

import ui

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = ui.StartupUI()
    sys.exit(app.exec())
