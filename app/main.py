import sys

from PyQt6.QtWidgets import QApplication

from app.application import PyComlApplication

_application_storage: set[PyComlApplication] = set()


def start_application() -> int:
    global _application_storage
    app = QApplication(sys.argv)
    # No logo for now, stay tuned
    # app.setWindowIcon(QIcon("img/Logo PyCommonist.svg"))
    # This variable should be alive, otherwise it will be destroyed by GC
    _application_storage.add(PyComlApplication())
    return app.exec()
