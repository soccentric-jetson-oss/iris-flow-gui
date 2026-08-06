"""Settings page for connection configuration."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame
)
from PySide6.QtCore import Qt
from src.theme import (
    TITLE_STYLE, SUBTITLE_STYLE, SECTION_TITLE_STYLE,
    BIG_BUTTON_STYLE, CARD_STYLE, INPUT_STYLE,
    MACOS_TEXT, MACOS_TEXT_SECONDARY, MACOS_BLUE, MACOS_GREEN, MACOS_RED,
)


class SettingsPage(QWidget):
    """Connection and application settings."""

    def __init__(self, client, parent=None):
        super().__init__(parent)
        self._client = client

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)

        # ── Header ─────────────────────────────────────────────────────
        header = QLabel("Settings")
        header.setStyleSheet(TITLE_STYLE)
        layout.addWidget(header)

        desc = QLabel("Configure server connection and application preferences.")
        desc.setStyleSheet(SUBTITLE_STYLE)
        layout.addWidget(desc)

        # ── Connection settings ────────────────────────────────────────
        conn_frame = QFrame()
        conn_frame.setStyleSheet(CARD_STYLE)
        conn_layout = QVBoxLayout(conn_frame)
        conn_layout.setSpacing(12)

        conn_title = QLabel("Server Connection")
        conn_title.setStyleSheet(SECTION_TITLE_STYLE)
        conn_layout.addWidget(conn_title)

        # Address row
        addr_row = QHBoxLayout()
        addr_row.setSpacing(12)
        addr_row.addWidget(QLabel("Server Address:"))
        self.address_input = QLineEdit("localhost:50052")
        self.address_input.setStyleSheet(INPUT_STYLE)
        self.address_input.setMinimumWidth(300)
        addr_row.addWidget(self.address_input)
        addr_row.addStretch()
        conn_layout.addLayout(addr_row)

        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setStyleSheet(BIG_BUTTON_STYLE)
        self.connect_btn.clicked.connect(self._on_connect)
        btn_row.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.setStyleSheet(
            f"QPushButton {{background: {MACOS_RED}; color: white; border: none; "
            f"border-radius: 12px; padding: 16px 32px; font-size: 15px; font-weight: 600; "
            f"min-width: 180px; min-height: 48px;}}"
            f"QPushButton:hover {{background: #C62828;}}"
        )
        self.disconnect_btn.clicked.connect(self._on_disconnect)
        btn_row.addWidget(self.disconnect_btn)

        btn_row.addStretch()
        conn_layout.addLayout(btn_row)

        # Status
        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setStyleSheet(
            f"color: {MACOS_RED}; font-size: 13px; padding: 4px 0;"
        )
        conn_layout.addWidget(self.status_label)

        layout.addWidget(conn_frame)
        layout.addStretch()

    def _on_connect(self):
        self._client.connect()
        if self._client.connected:
            self.status_label.setText("Status: Connected")
            self.status_label.setStyleSheet(
                f"color: {MACOS_GREEN}; font-size: 13px; padding: 4px 0;"
            )

    def _on_disconnect(self):
        self._client.disconnect()
        self.status_label.setText("Status: Disconnected")
        self.status_label.setStyleSheet(
            f"color: {MACOS_RED}; font-size: 13px; padding: 4px 0;"
        )
