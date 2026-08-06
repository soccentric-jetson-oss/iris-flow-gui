"""Iris Flow GUI - Entry point.

Thin entry point that creates the QApplication and launches the
main window. All UI logic lives in src.app.MainWindow.
"""

import sys
from PySide6.QtWidgets import QApplication
from src.app import MainWindow


def main():
    """Create and run the Iris Flow GUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Iris Flow")
    app.setOrganizationName("SoC Centric")
    app.setApplicationVersion("0.1.0")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
