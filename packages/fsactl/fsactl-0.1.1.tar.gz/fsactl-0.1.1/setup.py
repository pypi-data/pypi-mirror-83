# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fsactl', 'fsactl.handlers', 'fsactl.workers']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.11,<4.0.0',
 'Jinja2>=2.11.2,<3.0.0',
 'PyYaml>=5.3.1,<6.0.0',
 'coloredlogs>=14.0,<15.0',
 'semver>=2.13.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

extras_require = \
{'docs': ['sphinx>=3.2.1,<4.0.0',
          'sphinx_rtd_theme>=0.5.0,<0.6.0',
          'sphinx-autodoc-typehints>=1.11.1,<2.0.0',
          'sphinxcontrib-programoutput>=0.16,<0.17']}

entry_points = \
{'console_scripts': ['fsactl = fsactl.app:main']}

setup_kwargs = {
    'name': 'fsactl',
    'version': '0.1.1',
    'description': 'Install and update MSFS2020 addons',
    'long_description': '![GitHub](https://img.shields.io/github/license/MichaelSasser/fsactl?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fsactl?style=flat-square)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/fsactl?style=flat-square)\n![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/michaelsasser/fsactl?style=flat-square)\n![GitHub Release Date](https://img.shields.io/github/release-date/michaelsasser/fsactl?style=flat-square)\n![PyPI - Status](https://img.shields.io/pypi/status/fsactl?style=flat-square)\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/michaelsasser/fsactl?style=flat-square)\n\n# MS FlightSimulator 2020 Addon Control\n\nfsactl is a program to download, install, update, build and manage your FlightSimulator addons.\n\n## Development\n\nThis program is currently under development.\n\n## Installation\n\nfsactl is written in Python. The installation is straight forward. Just run ``pip install fsactl``. fsactl will be installd from the [Python Package Index (PyPi)](https://pypi.org/project/fsactl/).\n\nYou will find more information in the documentation.\n\n## Configuration File\n\nCreate a directory named fsactl in your My Documents directory and create a file called config.yaml in it\nwith a configuration like the following:\n\n```yaml\n---\n\n# This is a comment\n\nmsfs:\n  addon_dir: E:/MSFS-ADDONS  # A directory where your addons can be stored and managed\n  community_dir: E:/MSFS/Community  # Your community folder\n  addons:\n    - github: pimarc/pms50-gns530   # A prebuild addon from github\n    - github: lmk02/B787-XE  # A nother one\n    - github: saltysimulations/salty-747  # This addon needs a build step\n      build:\n        - path: "{{ addon_path }}"  # build directory\n          command: python build.py  # build command\n    - github: r9r-dev/fs2020-vl3-rotax915  # This addon must be build in two steps\n      build:\n        - path: "{{ addon_path }}"  # first build directory\n          command: update-layout.bat  # first build command\n        - path: "{{ addon_path }}/community-vl3rotax915"  # second build directory\n          command: "python {{ addon_path }}/build.py"  # second build command\n```\n\nBe sure to use slashs `/` instead of backslashs in all paths.\n\nYou will get a more detailed Documentation to this in the near future.\n\n## Usage\n\n```\n$ fsactl\nusage: fsactl [-h] [--version] [-d] {update,make,install} ...\n\npositional arguments:\n  {update,make,install}\n    update              Update and build addons\n    make                Force to rebuild the addons\n    install             Install addons\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --version             show program\'s version number and exit\n  -d, --debug           Enables debugging mode.\n```\n\n## Semantic Versioning\n\nThis repository uses [SemVer](https://semver.org/) for its release\ncycle.\n\n## Branching Model\n\nThis repository uses the\n[git-flow](https://danielkummer.github.io/git-flow-cheatsheet/index.html)\nbranching model by [Vincent Driessen](https://nvie.com/about/).\nIt has two branches with infinite lifetime:\n\n* [master](https://github.com/MichaelSasser/fsactl/tree/master)\n* [develop](https://github.com/MichaelSasser/fsactl/tree/develop)\n\nThe master branch gets updated on every release. The develop branch is the\nmerging branch.\n\n## License\nCopyright &copy; 2020 Michael Sasser <Info@MichaelSasser.org>. Released under\nthe GPLv3 license.\n',
    'author': 'Michael Sasser',
    'author_email': 'Michael@MichaelSasser.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://michaelsasser.github.io/fsactl/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
