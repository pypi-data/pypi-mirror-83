# pdftty

A PDF viewer for the terminal.


## Installation

```bash
$ pip install pdftty
```

Make sure to also install [libcaca](https://github.com/cacalabs/libcaca) if you want to use the `CACA` rendering engine.


## Usage

```bash
$ pdftty --help
Usage: pdftty [OPTIONS] <file>

  View PDFs in the terminal.

Options:
  --page INTEGER               Page of PDF to open.
  --render-engine [ANSI|CACA]  Which engine to use to render PDF page as text.
  --help                       Show this message and exit.
```





https://github.com/Belval/pdf2image
https://github.com/djentleman/imgrender/blob/master/imgrender/main.py


## Urwid tips:

* Widget classes: http://urwid.org/manual/widgets.html
* Widget reference: http://urwid.org/reference/widget.html


## poetry tipps

poetry install
poetry shell
\# do tests
python -m pdftty.main test.pdf
