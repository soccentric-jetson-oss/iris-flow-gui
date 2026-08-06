"""Iris Flow GUI - Main application window.

Assembles all widgets (header, stream controls, ISP panel, status)
and wires them to the gRPC client.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel
)
from PySide6.QtCore import QTimer

from src.client.client import IrisFlowClient
from src.widgets.header import HeaderWidget
from src.widgets.stream_controls import StreamControls
from src.widgets.isp_controls import IspControls


class IrisFlowApp(QMainWindow):
    """Main application window for Iris Flow GUI."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iris Flow")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 750)

        # ── gRPC client ────────────────────────────────────────────────
        self._client = IrisFlowClient()

        # ── Build UI ───────────────────────────────────────────────────
        self._setup_ui()
        self._connect_signals()

        # ── Periodic refresh ──────────────────────────────────────────
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(2000)

        # ── Initial connection ────────────────────────────────────────
        self._client.connect()
        self._header.set_connected(self._client.connected)

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self._header = HeaderWidget()
        layout.addWidget(self._header)

        # Content area
        content = QWidget()
        content.setStyleSheet("background: #f5f5f5;")
        cl = QVBoxLayout(content)
        cl.setContentsMargins(24, 20, 24, 20)
        cl.setSpacing(16)

        # Stream controls
        self._stream_ctrl = StreamControls()
        cl.addLayout(self._stream_ctrl.layout)

        # ISP controls
        self._isp_ctrl = IspControls()
        cl.addWidget(self._isp_ctrl.frame)

        # Status text
        self._status_text = QLabel("Status: Idle")
        self._status_text.setStyleSheet("color:#616161; font-size:12px;")
        cl.addWidget(self._status_text)
        cl.addStretch()

        layout.addWidget(content, 1)

    def _connect_signals(self):
        self._stream_ctrl.start_clicked.connect(self._on_start_stream)
        self._stream_ctrl.stop_clicked.connect(self._on_stop_stream)
        self._isp_ctrl.apply_clicked.connect(self._on_apply_isp)

    def _refresh(self):
        if not self._client.connected:
            self._client.connect()
            self._header.set_connected(self._client.connected)
            return

        status = self._client.get_status()
        state_str = "Running" if status["state"] else "Stopped"
        self._status_text.setText(
            f"Status: Sensor={status['sensor']} "
            f"FPS={status['fps']} State={state_str}"
        )

    def _on_start_stream(self):
        result = self._client.start_stream()
        if result["success"]:
            self._status_text.setText("Stream started")
        else:
            self._status_text.setText(f"Error: {result['error']}")

    def _on_stop_stream(self):
        result = self._client.stop_stream()
        if result["success"]:
            self._status_text.setText("Stream stopped")
        else:
            self._status_text.setText(f"Error: {result['error']}")

    def _on_apply_isp(self, values: dict):
        result = self._client.set_isp(
            brightness=values.get("brightness", 128),
            contrast=values.get("contrast", 128),
            saturation=values.get("saturation", 128),
        )
        if result["success"]:
            self._status_text.setText("ISP settings applied")
        else:
            self._status_text.setText(f"ISP failed: {result['error']}")
