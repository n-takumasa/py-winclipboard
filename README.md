# py-winclipboard

## Usage

### inspect clipboard data

```py
import winclipboard; winclipboard.inspect()
```

### copy text to clipboard

```py
import winclipboard

with winclipboard.clipboard() as clip:
    clip.set_text("spam")
```

## Develop

* hatch run python -X dev -m IPython
* hatch run python -m winclipboard
* hatch fmt --check --sync
  * ruff check --config ruff_all.toml
* hatch run types:check
* hatch test
* coverage
  * hatch test -c; hatch run coverage html; start htmlcov\index.html
