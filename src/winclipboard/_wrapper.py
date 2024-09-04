import contextlib
import ctypes
from collections.abc import Generator
from ctypes.wintypes import HGLOBAL, LPVOID
from typing import Any

from winclipboard import _nativemethods


@contextlib.contextmanager
def global_lock(handle: HGLOBAL) -> Generator[LPVOID, Any, None]:
    try:
        yield _nativemethods.GlobalLock(handle)
    finally:
        try:
            _nativemethods.GlobalUnlock(handle)
        except OSError as e:
            if e.winerror != 0:
                raise


def global_size(handle: HGLOBAL) -> int:
    flags = _nativemethods.GlobalFlags(handle)
    if flags & _nativemethods.GMEM_DISCARDED:
        return 0
    try:
        return _nativemethods.GlobalSize(handle)
    except OSError:
        ctypes.set_last_error(0)
        return 0


def get_format_name(format_id: int) -> str:
    for n in range(5, 32):
        count = 2**n
        buffer = ctypes.create_unicode_buffer(count)
        result = _nativemethods.GetClipboardFormatName(format_id, buffer, count)
        if result < count - 1:
            break
    else:
        # TODO: max size
        raise NotImplementedError
    return buffer.value
