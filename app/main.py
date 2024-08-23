import sys

from PyCommonist import PyCommonist
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    # No logo for now, stay tuned
    # app.setWindowIcon(QIcon("img/Logo PyCommonist.svg"))
    PyCommonist()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
