"""Iris Flow GUI - Stream control buttons.

Provides Start/Stop stream buttons with styled appearance.
"""

from PySide6.QtWidgets import QHBoxLayout, QPushButton
from PySide6.QtCore import Signal, QObject


class StreamControls(QObject):
    """Horizontal row of stream control buttons."""

    start_clicked = Signal()
    stop_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QHBoxLayout()
        self._build_ui()

    def _build_ui(self):
        self.start_btn = QPushButton("▶ Start Stream")
        self.start_btn.setStyleSheet(
            "background:#388E3C; color:white; border:none; "
            "border-radius:8px; padding:10px 24px; font-weight:bold;"
        )
        self.start_btn.clicked.connect(self.start_clicked.emit)
        self._layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("■ Stop Stream")
        self.stop_btn.setStyleSheet(
            "background:#D32F2F; color:white; border:none; "
            "border-radius:8px; padding:10px 24px; font-weight:bold;"
        )
        self.stop_btn.clicked.connect(self.stop_clicked.emit)
        self._layout.addWidget(self.stop_btn)

        self._layout.addStretch()

    @property
    def layout(self) -> QHBoxLayout:
        return self._layout
