import contextlib
import ctypes
import weakref
from ctypes.wintypes import HWND
from typing import ClassVar, Literal

from winclipboard import _nativemethods
from winclipboard._format import CF, _FormatType
from winclipboard._wrapper import global_lock, global_size


class Clipboard:
    instance: "ClassVar[Clipboard | None]" = None
    __slots__ = ()

    def __new__(cls) -> "Clipboard":
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def empty(self) -> None:
        _nativemethods.EmptyClipboard()

    def get(self, fmt: _FormatType) -> tuple[int, bytes | None]:
        fmt_id = CF.get_id(fmt)
        try:
            handle = _nativemethods.GetClipboardData(fmt_id)
        except OSError as e:
            if e.winerror == 0:
                return (0, None)
            raise
        size = global_size(handle)
        if size == 0:
            return (0, b"")
        buffer = ctypes.create_string_buffer(size)
        with global_lock(handle) as pointer:
            ctypes.memmove(buffer, pointer, size)
        return (size, buffer.raw)

    def set(self, fmt: _FormatType, data: bytes | None) -> None:
        self.empty()
        if data is None:
            try:
                _nativemethods.SetClipboardData(CF.get_id(fmt), None)
            except OSError as e:
                if e.winerror == 0:
                    return
                raise
            return
        size = len(data)
        handle = _nativemethods.GlobalAlloc(_nativemethods.GMEM_MOVEABLE, size)
        if size:
            with global_lock(handle) as pointer:
                ctypes.memmove(pointer, ctypes.c_char_p(data), size)
        _nativemethods.SetClipboardData(CF.get_id(fmt), handle)

    def set_text(self, text: str) -> None:
        self.set(CF.UNICODETEXT, f"{text}\x00".encode("utf-16le"))

    def enum_formats(self) -> list[int]:
        fmt = 0
        result = []

        count = _nativemethods.CountClipboardFormats()
        for _ in range(count):
            fmt = _nativemethods.EnumClipboardFormats(fmt)
            result.append(fmt)
        return result


class clipboard:
    def __init__(self, hwnd: HWND | None = None) -> None:
        self._opened: bool = False
        self.hwnd: HWND | None = hwnd
        self._myhwnd: HWND | None = None

    def __enter__(self) -> Clipboard:
        self.open()
        return Clipboard()

    def __exit__(self, *exc: object) -> Literal[False]:
        self.close()
        return False

    @staticmethod
    def _window() -> HWND:
        assert ctypes.get_last_error() == 0, ctypes.WinError(ctypes.get_last_error())
        hwnd = _nativemethods.CreateWindowEx(
            0,
            "Static",
            "",
            0,
            0,
            0,
            0,
            0,
            _nativemethods.HWND_MESSAGE,
            None,
            None,
            None,
        )
        # TODO: ERROR_INVALID_WINDOW_HANDLE (1400) を解決したい
        ctypes.set_last_error(0)
        assert ctypes.get_last_error() == 0, ctypes.WinError(ctypes.get_last_error())
        return hwnd

    @staticmethod
    def _force_close() -> None:
        with contextlib.suppress(Exception):
            _nativemethods.CloseClipboard()
            ctypes.set_last_error(0)

    def open(self) -> None:
        if not self._opened:
            if self.hwnd:
                hwnd = self.hwnd
            else:
                hwnd = self._myhwnd = self._window()
            _nativemethods.OpenClipboard(hwnd)
            self._opened = True
            self._finalizer = weakref.finalize(self, self._force_close)

    def close(self) -> None:
        if self._opened:
            _nativemethods.CloseClipboard()
            if self._myhwnd is not None:
                _nativemethods.DestroyWindow(self._myhwnd)
                self._myhwnd = None
            self._opened = False
            self._finalizer.detach()
