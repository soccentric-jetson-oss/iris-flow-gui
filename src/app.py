"""Iris Flow GUI - Main application window.

macOS-style design with complete menu bar, sidebar navigation,
and stacked pages. Assembles all widgets and wires signals.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QMessageBox
)
from PySide6.QtCore import QTimer

from src.client.client import IrisFlowClient
from src.sidebar import SidebarWidget
from src.menu import setup_menu_bar
from src.pages.dashboard import DashboardPage
from src.pages.controls import ControlsPage
from src.pages.settings import SettingsPage


class MainWindow(QMainWindow):
    """Main application window with menu bar, sidebar, and stacked pages."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iris Flow")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 800)

        # ── gRPC client ────────────────────────────────────────────────
        self._client = IrisFlowClient()

        # ── Menu bar ──────────────────────────────────────────────────
        setup_menu_bar(self)

        # ── Central widget: sidebar + pages ─────────────────────────────
        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = SidebarWidget()
        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage(self._client)
        self.controls_page = ControlsPage(self._client)
        self.settings_page = SettingsPage(self._client)

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.controls_page)
        self.pages.addWidget(self.settings_page)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)

        self.setCentralWidget(central)

        # ── Connect signals ─────────────────────────────────────────────
        self.sidebar.navigation_changed.connect(self.pages.setCurrentIndex)
        self.dashboard_page.connect_requested.connect(self._on_connect)
        self.dashboard_page.disconnect_requested.connect(self._on_disconnect)

        # ── Periodic refresh ───────────────────────────────────────────
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(2000)

        # ── Initial connection ─────────────────────────────────────────
        self._client.connect()
        self.sidebar.set_connected(self._client.connected)

    # ── Navigation ─────────────────────────────────────────────────────

    def navigate_to(self, index: int):
        """Navigate to a specific page by index."""
        self.pages.setCurrentIndex(index)
        self.sidebar._on_navigate(index)

    # ── Menu bar handlers ──────────────────────────────────────────────

    def on_new_connection(self):
        """Open a new connection dialog."""
        self.navigate_to(2)  # Settings page

    def on_undo(self):
        pass

    def on_redo(self):
        pass

    def on_cut(self):
        pass

    def on_copy(self):
        pass

    def on_paste(self):
        pass

    def on_select_all(self):
        pass

    def on_toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def on_toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())

    def on_connect(self):
        self._on_connect()

    def on_disconnect(self):
        self._on_disconnect()

    def on_refresh(self):
        self._refresh()

    def on_export_data(self):
        QMessageBox.information(self, "Export", "Export feature coming soon.")

    def on_about(self):
        QMessageBox.about(
            self, "About Iris Flow",
            "Iris Flow v0.1.0\n\n"
            "Vision Pipeline Control for NVIDIA Jetson AGX Orin\n\n"
            "Copyright (c) 2026 SoC Centric LLC"
        )

    def on_documentation(self):
        QMessageBox.information(self, "Documentation",
                                "See docs/ folder for documentation.")

    def on_report_issue(self):
        QMessageBox.information(self, "Report Issue",
                                "Please report issues at:\n"
                                "github.com/soccentric-jetson-oss/iris-flow-gui")

    # ── Internal handlers ──────────────────────────────────────────────

    def _on_connect(self):
        self._client.connect()
        self.sidebar.set_connected(self._client.connected)

    def _on_disconnect(self):
        self._client.disconnect()
        self.sidebar.set_connected(False)

    def _refresh(self):
        if not self._client.connected:
            self._client.connect()
            self.sidebar.set_connected(self._client.connected)
            return
        self.dashboard_page.refresh()
