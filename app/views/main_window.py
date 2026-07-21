import logging

import customtkinter as ctk

from app.constants import APP_NAME, APP_VERSION
from app.viewmodels.app_viewmodel import AppViewModel
from app.views.dashboard_tab import DashboardTab
from app.views.history_tab import HistoryTab
from app.views.large_display_window import LargeDisplayWindow
from app.views.settings_tab import SettingsTab

logger = logging.getLogger(__name__)


class MainWindow:
    """Root application window.  Owns the tab layout and the large-display overlay."""

    def __init__(self, viewmodel: AppViewModel) -> None:
        self._vm = viewmodel
        self._large_display: LargeDisplayWindow | None = None

        ctk.set_appearance_mode(viewmodel.config.theme)
        ctk.set_default_color_theme("blue")

        self._root = ctk.CTk()
        self._root.title(f"{APP_NAME}  v{APP_VERSION}")
        self._root.geometry("1280x780")
        self._root.minsize(960, 640)

        self._build_header()
        self._build_tabs()
        self._bind_keys()

        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------------ #
    # Layout                                                              #
    # ------------------------------------------------------------------ #

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self._root, height=48, corner_radius=0, fg_color=("#111827", "#111827"))
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text=f"  💽  {APP_NAME}",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w",
        ).pack(side="left", padx=16)

        self._usb_pill = ctk.CTkLabel(
            header,
            text="⚠️ No USB",
            font=ctk.CTkFont(size=12),
            text_color="#f59e0b",
            anchor="e",
        )
        self._usb_pill.pack(side="right", padx=16)

        ctk.CTkLabel(
            header,
            text="F11 = Large Display  ·  ESC = Exit",
            font=ctk.CTkFont(size=11),
            text_color="#444444",
            anchor="e",
        ).pack(side="right", padx=8)

        self._vm.subscribe(
            "usb_status_changed",
            lambda path: self._root.after(0, lambda p=path: self._update_usb_pill(p)),
        )

    def _build_tabs(self) -> None:
        self._tabs = ctk.CTkTabview(self._root, corner_radius=8)
        self._tabs.pack(fill="both", expand=True, padx=12, pady=(4, 12))

        self._tabs.add("🏠  Dashboard")
        self._tabs.add("📋  History")
        self._tabs.add("⚙️  Settings")

        DashboardTab(
            parent=self._tabs.tab("🏠  Dashboard"),
            viewmodel=self._vm,
        )
        HistoryTab(
            parent=self._tabs.tab("📋  History"),
            viewmodel=self._vm,
        )
        SettingsTab(
            parent=self._tabs.tab("⚙️  Settings"),
            viewmodel=self._vm,
        )

    def _bind_keys(self) -> None:
        self._root.bind("<F11>", self._toggle_large_display)

    # ------------------------------------------------------------------ #
    # Header USB pill                                                     #
    # ------------------------------------------------------------------ #

    def _update_usb_pill(self, path) -> None:
        if path:
            self._usb_pill.configure(
                text=f"💾  {path}",
                text_color="#22c55e",
            )
        else:
            self._usb_pill.configure(
                text="⚠️  No USB",
                text_color="#f59e0b",
            )

    # ------------------------------------------------------------------ #
    # Large display                                                       #
    # ------------------------------------------------------------------ #

    def _toggle_large_display(self, _event=None) -> None:
        if self._large_display and self._large_display.is_alive():
            self._large_display.close()
            self._large_display = None
            return

        # Prefer the currently-processing job; fall back to last history entry
        sn, did = None, None
        job = self._vm.current_job
        if job and job.serial_number:
            sn, did = job.serial_number, job.device_id
        else:
            history = self._vm.history
            if history and history[0].serial_number:
                sn, did = history[0].serial_number, history[0].device_id

        self._large_display = LargeDisplayWindow(
            parent=self._root,
            sn=sn,
            device_id=did,
            font_size=self._vm.config.large_display_font_size,
        )

    # ------------------------------------------------------------------ #
    # Lifecycle                                                           #
    # ------------------------------------------------------------------ #

    def _on_close(self) -> None:
        logger.info("Shutting down application")
        self._vm.stop()
        self._root.destroy()

    def run(self) -> None:
        self._vm.start()
        self._root.mainloop()
