"""Iris Flow GUI - Camera/ISP control application."""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QLabel, QStackedWidget, QFrame, QStatusBar, QSlider, QSpinBox, QComboBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

import grpc
from src.client import iris_flow_pb2, iris_flow_pb2_grpc


class IrisFlowApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iris Flow")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 750)

        # gRPC client
        self.channel = None
        self.stub = None
        self.connected = False

        self._setup_ui()
        self._connect()

        # Refresh timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(2000)

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("background: #1a1a2e; border-bottom: 1px solid #2a2a4a;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 0, 20, 0)
        title = QLabel("Iris Flow — Vision Pipeline")
        title.setStyleSheet("color: #64b5f6; font-size: 16px; font-weight: bold;")
        hl.addWidget(title)
        hl.addStretch()
        self.status_label = QLabel("Disconnected")
        self.status_label.setStyleSheet("color: #f44336; font-size: 12px;")
        hl.addWidget(self.status_label)
        layout.addWidget(header)

        # Content
        content = QWidget()
        content.setStyleSheet("background: #0f0f1a;")
        cl = QVBoxLayout(content)
        cl.setContentsMargins(24, 20, 24, 20)
        cl.setSpacing(16)

        # Stream controls
        ctrl_row = QHBoxLayout()
        self.start_btn = QPushButton("▶ Start Stream")
        self.start_btn.setStyleSheet("background:#4caf50; color:white; border:none; border-radius:8px; padding:10px 24px; font-weight:bold;")
        self.start_btn.clicked.connect(self._start_stream)
        ctrl_row.addWidget(self.start_btn)

        self.stop_btn = QPushButton("■ Stop Stream")
        self.stop_btn.setStyleSheet("background:#f44336; color:white; border:none; border-radius:8px; padding:10px 24px; font-weight:bold;")
        self.stop_btn.clicked.connect(self._stop_stream)
        ctrl_row.addWidget(self.stop_btn)
        ctrl_row.addStretch()
        cl.addLayout(ctrl_row)

        # ISP controls
        isp_frame = QFrame()
        isp_frame.setStyleSheet("background:#1a1a2e; border:1px solid #2a2a4a; border-radius:12px; padding:16px;")
        isp_layout = QVBoxLayout(isp_frame)
        isp_title = QLabel("ISP Controls")
        isp_title.setStyleSheet("color:#e0e0e0; font-size:14px; font-weight:bold;")
        isp_layout.addWidget(isp_title)

        for name in ["Brightness", "Contrast", "Saturation"]:
            row = QHBoxLayout()
            label = QLabel(f"{name}:")
            label.setFixedWidth(100)
            label.setStyleSheet("color:#aaa;")
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 255)
            slider.setValue(128)
            slider.setStyleSheet("QSlider::groove:horizontal {background:#2a2a4a; height:4px; border-radius:2px;} QSlider::handle:horizontal {background:#64b5f6; width:16px; border-radius:8px; margin:-6px 0;}")
            row.addWidget(label)
            row.addWidget(slider, 1)
            isp_layout.addLayout(row)

        self.apply_isp_btn = QPushButton("Apply ISP Settings")
        self.apply_isp_btn.setStyleSheet("background:#64b5f6; color:#0f0f1a; border:none; border-radius:8px; padding:8px 20px; font-weight:bold;")
        self.apply_isp_btn.clicked.connect(self._apply_isp)
        isp_layout.addWidget(self.apply_isp_btn)
        cl.addWidget(isp_frame)

        # Status
        self.status_text = QLabel("Status: Idle")
        self.status_text.setStyleSheet("color:#888; font-size:12px;")
        cl.addWidget(self.status_text)
        cl.addStretch()

        layout.addWidget(content, 1)

    def _connect(self):
        try:
            self.channel = grpc.insecure_channel("localhost:50052")
            self.stub = iris_flow_pb2_grpc.IrisFlowStub(self.channel)
            resp = self.stub.HealthCheck(iris_flow_pb2.HealthRequest(), timeout=2)
            self.connected = resp.status == "SERVING"
            self.status_label.setText("Connected" if self.connected else "Disconnected")
            self.status_label.setStyleSheet("color:#4caf50; font-size:12px;" if self.connected else "color:#f44336; font-size:12px;")
        except Exception:
            self.connected = False
            self.status_label.setText("Disconnected")
            self.status_label.setStyleSheet("color:#f44336; font-size:12px;")

    def _refresh(self):
        if not self.connected:
            self._connect()
            return
        try:
            resp = self.stub.GetStatus(iris_flow_pb2.StatusRequest(), timeout=2)
            self.status_text.setText(f"Status: Sensor={resp.sensor} FPS={resp.fps} State={'Running' if resp.state else 'Stopped'}")
        except Exception:
            self.connected = False

    def _start_stream(self):
        if not self.stub: return
        try:
            cfg = iris_flow_pb2.StreamConfig(width=1920, height=1080, format=1, fps=30)
            resp = self.stub.StartStream(cfg, timeout=5)
            self.status_text.setText("Stream started" if resp.success else f"Error: {resp.error}")
        except Exception as e:
            self.status_text.setText(f"Error: {e}")

    def _stop_stream(self):
        if not self.stub: return
        try:
            resp = self.stub.StopStream(iris_flow_pb2.StreamRequest(), timeout=5)
            self.status_text.setText("Stream stopped" if resp.success else f"Error: {resp.error}")
        except Exception as e:
            self.status_text.setText(f"Error: {e}")

    def _apply_isp(self):
        if not self.stub: return
        try:
            cfg = iris_flow_pb2.IspConfig(brightness=128, contrast=128, saturation=128)
            resp = self.stub.SetIsp(cfg, timeout=5)
            self.status_text.setText("ISP settings applied" if resp.success else "ISP failed")
        except Exception as e:
            self.status_text.setText(f"Error: {e}")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Iris Flow")
    window = IrisFlowApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
