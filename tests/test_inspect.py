from winclipboard import clipboard, inspect, preserve_clipboard


def test_inspect():
    # TODO: copy image
    inspect()


@preserve_clipboard()
def test_inspect_empty():
    with clipboard() as clip:
        clip.empty()

    inspect()
