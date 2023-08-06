# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hausgemachtspotipy']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.3,<5.0', 'pandas>=1.1.3,<2.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'hausgemachtspotipy',
    'version': '0.1.4',
    'description': 'Access artist, album, and tracks details via Spotify Web API endpoints',
    'long_description': 'hausgemachtSpotiPy\n==================\n\n**hausgemachtspotipy** is a Python package that access music artists,\nalbums, and tracks, directly from the Spotify Data Catalogue via Spotify\nWeb API endpoints.\n\nInspired by the `SpotiPy <https://pypi.org/project/spotipy/>`__ Python\npackage, the **hausgemachtspotipy** package focuses on easily querying\nmusic artists, albums, and tracks from Spotify.\n\nInstallation\n------------\n\nTo install\n\n.. code:: python\n\n    pip install hausgemachtspotipy\n\nTo upgrade\n\n.. code:: python\n\n    pip install hausgemachtspotipy --upgrade\n\nQuick Start\n-----------\n\n**Import Libraries**\n\n::\n\n    import hausgemachtspotipy as haussp\n    import pandas as pd\n    import datetime\n    import math\n\n**Define credentials**\n\n::\n\n    client_id = "cd1845f23d914228b14f6bed139ee594"\n    client_secret = <insert secret key>\n\nDetails on obtaining Spotify API credentials, head to\n\n**Create Spotify API token**\n\n::\n\n    sp = haussp.SpotifyAPI(client_id, client_secret)\n\n**Find Artist\'s details**\n\n::\n\n    artists = sp.search(query="Justin Timberlake")\n    print(artists)\n\n',
    'author': 'Rich Leung',
    'author_email': 'kleung.hkg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
