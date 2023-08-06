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
    'version': '0.1.2',
    'description': 'Access artist, album, and tracks details via Spotify Web API endpoints',
    'long_description': "hausgemachtspotipy\n==================\n\n===================\nProject Description\n===================\n**hausgemachtspotipy** is a Python package that access music artists, albums, and tracks, directly from the Spotify Data Catalogue via Spotify Web API endpoints.\n\nInspired by the `SpotiPy <https://pypi.org/project/spotipy/>`_ Python package, the **hausgemachtspotipy** package focus on easily querying music artists, albums, and tracks.\n\n\n\n============\nInstallation\n============\n.. code-block:: python\n\n  pip install hausgemachtspotipy\n\n\nTo upgrade\n\n.. code-block:: python\n\n  pip install hausgemachtspotipy --upgrade\n\n\n\n=================\nList of Functions\n=================\n\n1. General Search.  This function retrieves Spotify Catalog information about albums, artists, playlists, tracks, shows or episodes that match a keyword string.  See Spotify's web API reference `here <https://developer.spotify.com/documentation/web-api/reference/search/search/>`_.\n\n  Search Type includes:\n    - Album\n    - Artist (default)\n    - Playlist\n    - Track\n    - Show\n    - Episode\n\n2. `get_artist()` Search for artist by artist's Spotify ID.  This function is directly related to Spotify `Get an Artist <https://developer.spotify.com/documentation/web-api/reference/artists/get-artist/>`_ end-point.\n\n3. `get_artist_albums` Search for artist's albums.  This function is directly related to Spotify's `Get an Artist Album <https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-albums/>`_ end-point.\n\n4. `get_album` Search for albums.  This function is directly related to Spotify's .\n\n5. `get_album_tracks` Search for details of an album.  This function is directly related to Spotify's .\n\n6. `get_track` Search for information about a track.  This function is directly related to Spotify's .\n7. `get_track_features` Retrieve all relevant information (features) about a track.  This function is directly related to Spotify's.",
    'author': 'Rich Leung',
    'author_email': 'kleung.hkg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
