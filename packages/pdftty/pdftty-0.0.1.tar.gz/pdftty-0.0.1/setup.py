# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdftty']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.0,<9.0.0',
 'ansicolors>=1.1.8,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'numpy>=1.19.2,<2.0.0',
 'pdf2image>=1.14.0,<2.0.0',
 'urwid>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['pdftty = pdftty:main']}

setup_kwargs = {
    'name': 'pdftty',
    'version': '0.0.1',
    'description': 'A PDF viewer for the terminal',
    'long_description': '# pdftty\n\nA PDF viewer for the terminal.\n\n\n## Installation\n\n```bash\n$ pip install pdftty\n```\n\nMake sure to also install [libcaca](https://github.com/cacalabs/libcaca) if you want to use the `CACA` rendering engine.\n\n\n## Usage\n\n```bash\n$ pdftty --help\nUsage: pdftty [OPTIONS] <file>\n\n  View PDFs in the terminal.\n\nOptions:\n  --page INTEGER               Page of PDF to open.\n  --render-engine [ANSI|CACA]  Which engine to use to render PDF page as text.\n  --help                       Show this message and exit.\n```\n\n\n\n\n\nhttps://github.com/Belval/pdf2image\nhttps://github.com/djentleman/imgrender/blob/master/imgrender/main.py\n\n\n## Urwid tips:\n\n* Widget classes: http://urwid.org/manual/widgets.html\n* Widget reference: http://urwid.org/reference/widget.html\n\n\n## poetry tipps\n\npoetry install\npoetry shell\n\\# do tests\npython -m pdftty.main test.pdf\n',
    'author': 'kpj',
    'author_email': 'kpjkpjkpjkpjkpjkpj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kpj/pdftty',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
