# ruff: noqa: A002, ARG001 N802, N803, PLR0913, PLR0917
import ctypes
from ctypes import Array, c_int, c_size_t, c_wchar
from ctypes.wintypes import (
    BOOL,
    DWORD,
    HANDLE,
    HGLOBAL,
    HINSTANCE,
    HMENU,
    HWND,
    LPCWSTR,
    LPVOID,
    LPWSTR,
    UINT,
)
from typing import TYPE_CHECKING

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
user32 = ctypes.WinDLL("user32", use_last_error=True)

GMEM_FIXED = 0x0000
GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040
GMEM_DISCARDED = 0x4000
GMEM_INVALID_HANDLE = 0x8000

GHND = GMEM_MOVEABLE | GMEM_ZEROINIT
GPTR = GMEM_FIXED | GMEM_ZEROINIT

HWND_MESSAGE = HWND(0xFFFFFFFFFFFFFFFD)

if TYPE_CHECKING:
    # winbase.h
    def GlobalAlloc(uFlags: int, dwBytes: int, /) -> HGLOBAL: ...
    def GlobalFlags(hMem: HGLOBAL, /) -> int: ...
    def GlobalFree(hMem: HGLOBAL, /) -> HGLOBAL: ...
    def GlobalLock(hMem: HGLOBAL, /) -> LPVOID: ...
    def GlobalSize(hMem: HGLOBAL, /) -> int: ...
    def GlobalUnlock(hMem: HGLOBAL, /) -> int: ...

    # winuser.h
    def CloseClipboard() -> int: ...
    def CountClipboardFormats() -> int: ...
    def EmptyClipboard() -> int: ...
    def EnumClipboardFormats(format: int, /) -> int: ...
    def GetClipboardData(uFormat: int, /) -> HANDLE: ...
    def GetClipboardFormatName(
        format: int,
        lpszFormatName: Array[c_wchar],
        cchMaxCount: int,
    ) -> int: ...
    def IsClipboardFormatAvailable(format: int, /) -> int: ...
    def OpenClipboard(hWndNewOwner: HWND | None, /) -> int: ...
    def RegisterClipboardFormat(lpszFormat: str, /) -> int: ...
    def SetClipboardData(uFormat: int, hMem: HANDLE | None, /) -> HANDLE: ...
    def CreateWindowEx(
        dwExStyle: int,
        lpClassName: str,
        lpWindowName: str,
        dwStyle: int,
        X: int,
        Y: int,
        nWidth: int,
        nHeight: int,
        hWndParent: HWND | None,
        hMenu: HMENU | None,
        hInstance: HINSTANCE | None,
        lpParam: LPVOID | None,
        /,
    ) -> HWND: ...
    def DestroyWindow(hWnd: HWND) -> int: ...


def errcheck_fail_on_zero(result, func, arguments):
    if not result:
        raise ctypes.WinError(code=ctypes.get_last_error())
    return result


def errcheck_fail_on_nonzero(result, func, arguments):
    if result:
        raise ctypes.WinError(code=ctypes.get_last_error())
    return result


def errcheck_count(result, func, arguments):
    if not result and (code := ctypes.get_last_error()) != 0:
        raise ctypes.WinError(code)
    return result


# winbase.h

# DECLSPEC_ALLOCATOR HGLOBAL GlobalAlloc(
#   [in] UINT   uFlags,
#   [in] SIZE_T dwBytes
# );
GlobalAlloc = kernel32.GlobalAlloc
GlobalAlloc.restype = HGLOBAL
GlobalAlloc.argtypes = [UINT, c_size_t]
GlobalAlloc.errcheck = errcheck_fail_on_zero

# UINT GlobalFlags(
#   [in] HGLOBAL hMem
# );
GlobalFlags = kernel32.GlobalFlags
GlobalFlags.restype = UINT
GlobalFlags.argtypes = [HGLOBAL]

# HGLOBAL GlobalFree(
#   [in] _Frees_ptr_opt_ HGLOBAL hMem
# );
GlobalFree = kernel32.GlobalFree
GlobalFree.restype = HGLOBAL
GlobalFree.argtypes = [HGLOBAL]
GlobalFree.errcheck = errcheck_fail_on_nonzero

# LPVOID GlobalLock(
#   [in] HGLOBAL hMem
# );
GlobalLock = kernel32.GlobalLock
GlobalLock.restype = LPVOID
GlobalLock.argtypes = [HGLOBAL]
GlobalLock.errcheck = errcheck_fail_on_zero

# SIZE_T GlobalSize(
#   [in] HGLOBAL hMem
# );
GlobalSize = kernel32.GlobalSize
GlobalSize.restype = c_size_t
GlobalSize.argtypes = [HGLOBAL]
GlobalSize.errcheck = errcheck_fail_on_zero

# BOOL GlobalUnlock(
#   [in] HGLOBAL hMem
# );
GlobalUnlock = kernel32.GlobalUnlock
GlobalUnlock.restype = BOOL
GlobalUnlock.argtypes = [HGLOBAL]
GlobalUnlock.errcheck = errcheck_fail_on_zero

# winuser.h

# BOOL CloseClipboard();
CloseClipboard = user32.CloseClipboard
CloseClipboard.restype = BOOL
CloseClipboard.argtypes = []
CloseClipboard.errcheck = errcheck_fail_on_zero

# int CountClipboardFormats();
CountClipboardFormats = user32.CountClipboardFormats
CountClipboardFormats.restype = c_int
CountClipboardFormats.argtypes = []
CountClipboardFormats.errcheck = errcheck_count

# BOOL EmptyClipboard();
EmptyClipboard = user32.EmptyClipboard
EmptyClipboard.restype = BOOL
EmptyClipboard.argtypes = []
EmptyClipboard.errcheck = errcheck_fail_on_zero

# UINT EnumClipboardFormats(
#   [in] UINT format
# );
EnumClipboardFormats = user32.EnumClipboardFormats
EnumClipboardFormats.restype = UINT
EnumClipboardFormats.argtypes = [UINT]
EnumClipboardFormats.errcheck = errcheck_fail_on_zero

# HANDLE GetClipboardData(
#   [in] UINT uFormat
# );
GetClipboardData = user32.GetClipboardData
GetClipboardData.restype = HANDLE
GetClipboardData.argtypes = [UINT]
GetClipboardData.errcheck = errcheck_fail_on_zero

# int GetClipboardFormatNameW(
#   [in]  UINT   format,
#   [out] LPWSTR lpszFormatName,
#   [in]  int    cchMaxCount
# );
GetClipboardFormatName = user32.GetClipboardFormatNameW
GetClipboardFormatName.restype = c_int
GetClipboardFormatName.argtypes = [UINT, LPWSTR, c_int]
GetClipboardFormatName.errcheck = errcheck_fail_on_zero

# BOOL IsClipboardFormatAvailable(
#   [in] UINT format
# );
IsClipboardFormatAvailable = user32.IsClipboardFormatAvailable
IsClipboardFormatAvailable.restype = BOOL
IsClipboardFormatAvailable.argtypes = [UINT]
IsClipboardFormatAvailable.errcheck = errcheck_fail_on_zero

# BOOL OpenClipboard(
#   [in, optional] HWND hWndNewOwner
# );
OpenClipboard = user32.OpenClipboard
OpenClipboard.restype = BOOL
OpenClipboard.argtypes = [HWND]
OpenClipboard.errcheck = errcheck_fail_on_zero

# UINT RegisterClipboardFormatW(
#   [in] LPCWSTR lpszFormat
# );
RegisterClipboardFormat = user32.RegisterClipboardFormatW
RegisterClipboardFormat.restype = UINT
RegisterClipboardFormat.argtypes = [LPCWSTR]
RegisterClipboardFormat.errcheck = errcheck_fail_on_zero

# HANDLE SetClipboardData(
#   [in]           UINT   uFormat,
#   [in, optional] HANDLE hMem
# );
SetClipboardData = user32.SetClipboardData
SetClipboardData.restype = HANDLE
SetClipboardData.argtypes = [UINT, HANDLE]
SetClipboardData.errcheck = errcheck_fail_on_zero

# HWND CreateWindowExW(
#   [in]           DWORD     dwExStyle,
#   [in, optional] LPCWSTR   lpClassName,
#   [in, optional] LPCWSTR   lpWindowName,
#   [in]           DWORD     dwStyle,
#   [in]           int       X,
#   [in]           int       Y,
#   [in]           int       nWidth,
#   [in]           int       nHeight,
#   [in, optional] HWND      hWndParent,
#   [in, optional] HMENU     hMenu,
#   [in, optional] HINSTANCE hInstance,
#   [in, optional] LPVOID    lpParam
# );
CreateWindowEx = user32.CreateWindowExW
CreateWindowEx.restype = HWND
CreateWindowEx.argtypes = [
    DWORD,  # dwExStyle
    LPCWSTR,  # lpClassName
    LPCWSTR,  # lpWindowName
    DWORD,  # dwStyle
    c_int,  # X
    c_int,  # Y
    c_int,  # nWidth
    c_int,  # nHeight
    HWND,  # hWndParent
    HMENU,  # hMenu
    HINSTANCE,  # hInstance
    LPVOID,  # lpParam
]
CreateWindowEx.errcheck = errcheck_fail_on_zero

# BOOL DestroyWindow(
#   [in] HWND hWnd
# );
DestroyWindow = user32.DestroyWindow
DestroyWindow.restype = BOOL
DestroyWindow.argtypes = [HWND]
DestroyWindow.errcheck = errcheck_fail_on_zero
