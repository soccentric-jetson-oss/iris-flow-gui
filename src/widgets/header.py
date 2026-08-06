"""Iris Flow GUI - Header widget.

Displays the application title and connection status indicator.
"""

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PySide6.QtCore import Qt


class HeaderWidget(QFrame):
    """Top bar with title and connection status."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setStyleSheet(
            "background: #1a1a2e; border-bottom: 1px solid #2a2a4a;"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel("Iris Flow — Vision Pipeline")
        title.setStyleSheet(
            "color: #64b5f6; font-size: 16px; font-weight: bold;"
        )
        layout.addWidget(title)
        layout.addStretch()

        self.status_label = QLabel("Disconnected")
        self.status_label.setStyleSheet(
            "color: #f44336; font-size: 12px;"
        )
        layout.addWidget(self.status_label)

    def set_connected(self, connected: bool):
        """Update the connection status indicator."""
        if connected:
            self.status_label.setText("Connected")
            self.status_label.setStyleSheet(
                "color: #4caf50; font-size: 12px;"
            )
        else:
            self.status_label.setText("Disconnected")
            self.status_label.setStyleSheet(
                "color: #f44336; font-size: 12px;"
            )
