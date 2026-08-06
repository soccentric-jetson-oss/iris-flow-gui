"""Iris Flow GUI - ISP controls panel.

Provides sliders for brightness, contrast, and saturation tuning.
Emits a signal when the user clicks "Apply ISP Settings".
"""

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton
)
from PySide6.QtCore import Qt, Signal, QObject


class IspControls(QObject):
    """ISP tuning panel with brightness/contrast/saturation sliders."""

    apply_clicked = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._frame = QFrame()
        self._sliders = {}
        self._build_ui()

    def _build_ui(self):
        self._frame.setStyleSheet(
            "background:#ffffff; border:1px solid #e0e0e0; "
            "border-radius:12px; padding:16px;"
        )
        layout = QVBoxLayout(self._frame)

        title = QLabel("ISP Controls")
        title.setStyleSheet(
            "color:#212121; font-size:14px; font-weight:bold;"
        )
        layout.addWidget(title)

        for name in ["Brightness", "Contrast", "Saturation"]:
            row = QHBoxLayout()
            label = QLabel(f"{name}:")
            label.setFixedWidth(100)
            label.setStyleSheet("color:#616161;")

            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 255)
            slider.setValue(128)
            slider.setStyleSheet(
                "QSlider::groove:horizontal {background:#e0e0e0; "
                "height:4px; border-radius:2px;} "
                "QSlider::handle:horizontal {background:#1976D2; "
                "width:16px; border-radius:8px; margin:-6px 0;}"
            )
            self._sliders[name.lower()] = slider

            row.addWidget(label)
            row.addWidget(slider, 1)
            layout.addLayout(row)

        apply_btn = QPushButton("Apply ISP Settings")
        apply_btn.setStyleSheet(
            "background:#1976D2; color:#212121; border:none; "
            "border-radius:8px; padding:8px 20px; font-weight:bold;"
        )
        apply_btn.clicked.connect(self._on_apply)
        layout.addWidget(apply_btn)

    def _on_apply(self):
        values = {
            name: slider.value()
            for name, slider in self._sliders.items()
        }
        self.apply_clicked.emit(values)

    @property
    def frame(self) -> QFrame:
        return self._frame
