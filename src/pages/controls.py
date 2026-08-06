"""Controls page with ISP tuning sliders and stream configuration."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton,
    QSpinBox, QFrame
)
from PySide6.QtCore import Qt
from src.theme import (
    TITLE_STYLE, SUBTITLE_STYLE, SECTION_TITLE_STYLE,
    BIG_BUTTON_STYLE, CARD_STYLE, INPUT_STYLE,
    MACOS_TEXT, MACOS_TEXT_SECONDARY, MACOS_BLUE, MACOS_BORDER,
)


class ControlsPage(QWidget):
    """Stream configuration and ISP tuning controls."""

    def __init__(self, client, parent=None):
        super().__init__(parent)
        self._client = client

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)

        # ── Header ─────────────────────────────────────────────────────
        header = QLabel("Controls")
        header.setStyleSheet(TITLE_STYLE)
        layout.addWidget(header)

        desc = QLabel("Configure stream parameters and ISP tuning settings.")
        desc.setStyleSheet(SUBTITLE_STYLE)
        layout.addWidget(desc)

        # ── Stream configuration ───────────────────────────────────────
        stream_frame = QFrame()
        stream_frame.setStyleSheet(CARD_STYLE)
        stream_layout = QVBoxLayout(stream_frame)
        stream_layout.setSpacing(12)

        stream_title = QLabel("Stream Configuration")
        stream_title.setStyleSheet(SECTION_TITLE_STYLE)
        stream_layout.addWidget(stream_title)

        # Resolution row
        res_row = QHBoxLayout()
        res_row.setSpacing(12)
        res_row.addWidget(QLabel("Resolution:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(320, 7680)
        self.width_spin.setValue(1920)
        self.width_spin.setStyleSheet(INPUT_STYLE)
        res_row.addWidget(self.width_spin)
        res_row.addWidget(QLabel("x"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(240, 4320)
        self.height_spin.setValue(1080)
        self.height_spin.setStyleSheet(INPUT_STYLE)
        res_row.addWidget(self.height_spin)
        res_row.addStretch()
        stream_layout.addLayout(res_row)

        # FPS row
        fps_row = QHBoxLayout()
        fps_row.setSpacing(12)
        fps_row.addWidget(QLabel("Frame Rate:"))
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 240)
        self.fps_spin.setValue(30)
        self.fps_spin.setStyleSheet(INPUT_STYLE)
        fps_row.addWidget(self.fps_spin)
        fps_row.addStretch()
        stream_layout.addLayout(fps_row)

        layout.addWidget(stream_frame)

        # ── ISP Controls ───────────────────────────────────────────────
        isp_frame = QFrame()
        isp_frame.setStyleSheet(CARD_STYLE)
        isp_layout = QVBoxLayout(isp_frame)
        isp_layout.setSpacing(12)

        isp_title = QLabel("ISP Tuning")
        isp_title.setStyleSheet(SECTION_TITLE_STYLE)
        isp_layout.addWidget(isp_title)

        self._sliders = {}
        for name in ["Brightness", "Contrast", "Saturation", "Sharpness"]:
            row = QHBoxLayout()
            row.setSpacing(12)
            label = QLabel(f"{name}:")
            label.setFixedWidth(100)
            label.setStyleSheet(f"color: {MACOS_TEXT}; font-size: 13px;")
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 255)
            slider.setValue(128)
            slider.setStyleSheet(
                f"QSlider::groove:horizontal {{background: {MACOS_BORDER}; "
                f"height: 4px; border-radius: 2px;}} "
                f"QSlider::handle:horizontal {{background: {MACOS_BLUE}; "
                f"width: 16px; border-radius: 8px; margin: -6px 0;}}"
            )
            self._sliders[name.lower()] = slider
            row.addWidget(label)
            row.addWidget(slider, 1)
            isp_layout.addLayout(row)

        apply_btn = QPushButton("Apply ISP Settings")
        apply_btn.setStyleSheet(BIG_BUTTON_STYLE)
        apply_btn.clicked.connect(self._on_apply_isp)
        isp_layout.addWidget(apply_btn, alignment=Qt.AlignLeft)

        layout.addWidget(isp_frame)
        layout.addStretch()

    def _on_apply_isp(self):
        values = {name: slider.value() for name, slider in self._sliders.items()}
        self._client.set_isp(
            brightness=values.get("brightness", 128),
            contrast=values.get("contrast", 128),
            saturation=values.get("saturation", 128),
        )
