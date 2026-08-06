"""Dashboard page with big button boxes and status cards."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt
from src.theme import TITLE_STYLE, SUBTITLE_STYLE, MACOS_TEXT_SECONDARY
from src.widgets import BigButtonBox, MacCard


class DashboardPage(QWidget):
    """Main dashboard with big action buttons and live status cards."""

    connect_requested = Signal()
    disconnect_requested = Signal()

    def __init__(self, client, parent=None):
        super().__init__(parent)
        self._client = client

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)

        # ── Header ─────────────────────────────────────────────────────
        header = QLabel("Dashboard")
        header.setStyleSheet(TITLE_STYLE)
        layout.addWidget(header)

        desc = QLabel("Monitor and control the Iris Flow vision pipeline.")
        desc.setStyleSheet(SUBTITLE_STYLE)
        layout.addWidget(desc)

        # ── Big button boxes row ───────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)

        self.start_box = BigButtonBox(
            "Start Stream",
            "Begin capturing video from the connected camera sensor.\n"
            "Configure resolution and frame rate in Controls.",
            "▶  Start Stream",
            "primary"
        )
        self.start_box.button.clicked.connect(self._on_start)
        btn_row.addWidget(self.start_box)

        self.stop_box = BigButtonBox(
            "Stop Stream",
            "Halt the active video stream and release the camera.\n"
            "All pipeline resources will be cleaned up.",
            "■  Stop Stream",
            "danger"
        )
        self.stop_box.button.clicked.connect(self._on_stop)
        btn_row.addWidget(self.stop_box)

        layout.addLayout(btn_row)

        # ── Status cards row ───────────────────────────────────────────
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self.status_card = MacCard("Status", "Idle", "", "#616161")
        self.fps_card = MacCard("Frame Rate", "0", "fps")
        self.sensor_card = MacCard("Sensor", "N/A", "")
        self.latency_card = MacCard("Latency", "0", "ms")

        cards_row.addWidget(self.status_card)
        cards_row.addWidget(self.fps_card)
        cards_row.addWidget(self.sensor_card)
        cards_row.addWidget(self.latency_card)
        layout.addLayout(cards_row)

        layout.addStretch()

    def _on_start(self):
        result = self._client.start_stream()
        if result["success"]:
            self.status_card.set_value("Running")
            self.status_card.value_label.setStyleSheet(
                "color: #388E3C; font-size: 28px; font-weight: 700;"
            )

    def _on_stop(self):
        result = self._client.stop_stream()
        if result["success"]:
            self.status_card.set_value("Stopped")
            self.status_card.value_label.setStyleSheet(
                "color: #D32F2F; font-size: 28px; font-weight: 700;"
            )

    def refresh(self):
        """Update status cards with latest data from server."""
        if not self._client.connected:
            return
        status = self._client.get_status()
        self.fps_card.set_value(str(status["fps"]))
        self.sensor_card.set_value(status["sensor"])
        state_str = "Running" if status["state"] else "Stopped"
        self.status_card.set_value(state_str)
        if status["state"]:
            self.status_card.value_label.setStyleSheet(
                "color: #388E3C; font-size: 28px; font-weight: 700;"
            )
        else:
            self.status_card.value_label.setStyleSheet(
                "color: #616161; font-size: 28px; font-weight: 700;"
            )
