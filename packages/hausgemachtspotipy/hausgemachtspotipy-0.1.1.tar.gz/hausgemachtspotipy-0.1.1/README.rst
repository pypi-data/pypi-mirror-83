hausgemachtspotipy
==================

===================
Project Description
===================
**hausgemachtspotipy** is a Python package that access music artists, albums, and tracks, directly from the Spotify Data Catalogue via Spotify Web API endpoints.

Inspired by the `SpotiPy <https://pypi.org/project/spotipy/>`_ Python package, the **hausgemachtspotipy** package focus on easily querying music artists, albums, and tracks.



============
Installation
============
.. code-block:: python

  pip install hausgemachtspotipy


To upgrade

.. code-block:: python

  pip install hausgemachtspotipy --upgrade



=================
List of Functions
=================

1. General Search.  This function retrieves Spotify Catalog information about albums, artists, playlists, tracks, shows or episodes that match a keyword string.  See Spotify's web API reference `here <https://developer.spotify.com/documentation/web-api/reference/search/search/>`_.

  Search Type includes:
    - Album
    - Artist (default)
    - Playlist
    - Track
    - Show
    - Episode

2. `get_artist()` Search for artist by artist's Spotify ID.  This function is directly related to Spotify `Get an Artist <https://developer.spotify.com/documentation/web-api/reference/artists/get-artist/>`_ end-point.

3. `get_artist_albums` Search for artist's albums.  This function is directly related to Spotify's `Get an Artist Album <https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-albums/>`_ end-point.

4. `get_album` Search for albums.  This function is directly related to Spotify's .

5. `get_album_tracks` Search for details of an album.  This function is directly related to Spotify's .

6. `get_track` Search for information about a track.  This function is directly related to Spotify's .
7. `get_track_features` Retrieve all relevant information (features) about a track.  This function is directly related to Spotify's .