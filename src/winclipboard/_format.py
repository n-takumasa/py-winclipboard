# ruff: noqa: PIE796
import enum

from winclipboard import _nativemethods
from winclipboard._wrapper import get_format_name


class ClipboardFormat(enum.Enum):
    CF_TEXT = 1
    CF_BITMAP = 2
    CF_METAFILEPICT = 3
    CF_SYLK = 4
    CF_DIF = 5
    CF_TIFF = 6
    CF_OEMTEXT = 7
    CF_DIB = 8
    CF_PALETTE = 9
    CF_PENDATA = 10
    CF_RIFF = 11
    CF_WAVE = 12
    CF_UNICODETEXT = 13
    CF_ENHMETAFILE = 14
    CF_HDROP = 15
    CF_LOCALE = 16
    CF_DIBV5 = 17
    CF_MAX = 18

    TEXT = 1
    BITMAP = 2
    METAFILEPICT = 3
    SYLK = 4
    DIF = 5
    TIFF = 6
    OEMTEXT = 7
    DIB = 8
    PALETTE = 9
    PENDATA = 10
    RIFF = 11
    WAVE = 12
    UNICODETEXT = 13
    ENHMETAFILE = 14
    HDROP = 15
    LOCALE = 16
    DIBV5 = 17
    MAX = 18

    @classmethod
    def get_id(cls, x: "ClipboardFormat | str | int") -> int:
        if isinstance(x, int):
            return x
        if isinstance(x, ClipboardFormat):
            return x.value
        if x in cls.__members__:
            return cls[x].value
        if x.capitalize() in cls.__members__:
            return cls[x.capitalize()].value
        return _nativemethods.RegisterClipboardFormat(x)

    @classmethod
    def get_name(cls, x: "ClipboardFormat | str | int") -> str:
        if isinstance(x, str):
            return x
        if isinstance(x, ClipboardFormat):
            return x.name
        if 0 <= x <= cls.CF_MAX.value:
            return cls(x).name
        return get_format_name(x)


CF = ClipboardFormat

_FormatType = ClipboardFormat | str | int
