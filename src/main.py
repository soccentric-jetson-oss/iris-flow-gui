# SPDX-License-Identifier: MIT
"""
Iris Flow GUI - Application entry point.

Thin entry point that creates the QApplication and launches the
main window. All UI logic lives in src.app.IrisFlowApp.
"""

import sys
from PySide6.QtWidgets import QApplication
from src.app import IrisFlowApp


def main():
    """Create and run the Iris Flow GUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Iris Flow")
    window = IrisFlowApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
