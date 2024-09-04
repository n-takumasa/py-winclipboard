from winclipboard import CF, clipboard, preserve_clipboard


@preserve_clipboard()
def test_copy_text():
    data = "spam"
    ret = None
    with clipboard() as clip:
        clip.set_text(data)
        _, ret = clip.get(CF.UNICODETEXT)
        assert ret is not None
        assert data == ret.decode("utf-16le")[:-1]
