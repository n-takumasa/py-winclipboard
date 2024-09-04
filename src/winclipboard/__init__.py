import contextlib
import sys
from collections.abc import Generator
from typing import Any

from winclipboard._clipboard import clipboard
from winclipboard._format import CF, ClipboardFormat

if sys.platform != "win32":
    msg = """`sys.platform != "win32"` is not supported"""
    raise ImportError(msg)

del sys


def inspect(*, verbose: bool = False) -> None:
    import reprlib

    with clipboard() as clip:
        formats = clip.enum_formats()
        names = [CF.get_name(x) for x in formats]
        ds = [clip.get(x) for x in formats]
        size, data = [x[0] for x in ds], [x[1] for x in ds]

        # NOTE: >= py3.12
        # aRepr = reprlib.Repr(maxother=60)
        aRepr = reprlib.Repr()
        aRepr.maxother = 60

        try:
            import rich  # type: ignore[reportMissingImports]
            from rich.table import Table  # type: ignore[reportMissingImports]

            table = Table("format", "name", "size", "data")

            for f, n, s, d in zip(formats, names, size, data, strict=True):
                table.add_row(
                    repr(f),
                    n,
                    repr(s),
                    (repr(d) if verbose else aRepr.repr(d)) if d else "None",
                )
            rich.print(table)
        except ImportError:
            import pprint

            pprint.pp(
                [
                    {
                        "format": f,
                        "name": n,
                        "size": s,
                        "data": (d if verbose else aRepr.repr(d)) if d else None,
                    }
                    for f, n, s, d in zip(formats, names, size, data, strict=True)
                ],
            )


@contextlib.contextmanager
def preserve_clipboard() -> Generator[None, Any, None]:
    # TODO: win+shift+s の画像で死ぬ
    with clipboard() as clip:
        formats = clip.enum_formats()
        data = [clip.get(x)[1] for x in formats]
    try:
        yield
    finally:
        with clipboard() as clip:
            clip.empty()
            for f, d in zip(formats, data, strict=True):  # type: ignore[reportPossiblyUnboundVariable]
                clip.set(f, d)


__all__ = [
    "CF",
    "ClipboardFormat",
    "clipboard",
    "inspect",
    "preserve_clipboard",
]
