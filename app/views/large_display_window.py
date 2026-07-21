import customtkinter as ctk
from typing import Optional


class LargeDisplayWindow:
    """
    Fullscreen overlay showing S/N and ID in a very large font.
    Opened with F11; closed with ESC or F11 again.
    """

    def __init__(
        self,
        parent: ctk.CTk,
        sn: Optional[str],
        device_id: Optional[str],
        font_size: int = 96,
    ) -> None:
        self._window = ctk.CTkToplevel(parent)
        self._window.title("Large Display")
        self._window.attributes("-fullscreen", True)
        self._window.attributes("-topmost", True)
        self._window.configure(fg_color="#0a0a0a")

        self._window.bind("<Escape>", lambda _: self.close())
        self._window.bind("<F11>", lambda _: self.close())

        self._build(sn, device_id, font_size)
        self._window.focus_force()

    def _build(self, sn: Optional[str], device_id: Optional[str], font_size: int) -> None:
        outer = ctk.CTkFrame(self._window, fg_color="transparent")
        outer.place(relx=0.5, rely=0.5, anchor="center")

        if sn:
            ctk.CTkLabel(
                outer,
                text=sn,
                font=ctk.CTkFont(family="Consolas", size=font_size, weight="bold"),
                text_color="#f0f0f0",
            ).pack(pady=(0, 16))
        else:
            ctk.CTkLabel(
                outer,
                text="No data",
                font=ctk.CTkFont(size=font_size // 2),
                text_color="#555555",
            ).pack(pady=(0, 16))

        if device_id:
            ctk.CTkLabel(
                outer,
                text=f"({device_id})",
                font=ctk.CTkFont(family="Consolas", size=font_size, weight="bold"),
                text_color="#60a5fa",
            ).pack()

        ctk.CTkLabel(
            self._window,
            text="ESC  ·  Exit Large Display",
            font=ctk.CTkFont(size=14),
            text_color="#444444",
        ).place(relx=0.5, rely=0.95, anchor="center")

    def close(self) -> None:
        try:
            self._window.destroy()
        except Exception:
            pass

    def is_alive(self) -> bool:
        try:
            return self._window.winfo_exists()
        except Exception:
            return False
