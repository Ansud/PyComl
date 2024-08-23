import sys

from PyCommonist import PyCommonist
from PyQt6.QtWidgets import QApplication

_application_storage: set[PyCommonist] = set()


def main():
    global _application_storage
    app = QApplication(sys.argv)
    # No logo for now, stay tuned
    # app.setWindowIcon(QIcon("img/Logo PyCommonist.svg"))
    # This variable should be alive, otherwise it will be destroyed by GC
    _application_storage.add(PyCommonist())
    sys.exit(app.exec())
