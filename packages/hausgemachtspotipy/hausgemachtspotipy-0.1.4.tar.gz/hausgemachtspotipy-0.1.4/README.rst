hausgemachtSpotiPy
==================

**hausgemachtspotipy** is a Python package that access music artists,
albums, and tracks, directly from the Spotify Data Catalogue via Spotify
Web API endpoints.

Inspired by the `SpotiPy <https://pypi.org/project/spotipy/>`__ Python
package, the **hausgemachtspotipy** package focuses on easily querying
music artists, albums, and tracks from Spotify.

Installation
------------

To install

.. code:: python

    pip install hausgemachtspotipy

To upgrade

.. code:: python

    pip install hausgemachtspotipy --upgrade

Quick Start
-----------

**Import Libraries**

::

    import hausgemachtspotipy as haussp
    import pandas as pd
    import datetime
    import math

**Define credentials**

::

    client_id = "cd1845f23d914228b14f6bed139ee594"
    client_secret = <insert secret key>

Details on obtaining Spotify API credentials, head to

**Create Spotify API token**

::

    sp = haussp.SpotifyAPI(client_id, client_secret)

**Find Artist's details**

::

    artists = sp.search(query="Justin Timberlake")
    print(artists)

