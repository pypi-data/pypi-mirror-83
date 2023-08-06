#!/usr/bin/env python
# coding: utf-8

# In[1]:


import base64
import datetime
from urllib.parse import urlencode

import requests


# In[3]:


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None

    token_URL = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        METHOD: Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if (client_id is None) or (client_secret is None):
            raise Exception(
                "You must set a Client ID or a Client Secret with Spotify Developer Account."
            )

        # Convert Spotify Credentials from string to base64-bytes (decoded)
        client_creds = f"{client_id}:{client_secret}"  # type: String
        client_creds_b64 = base64.b64encode(client_creds.encode())  # type: Base64-Byte
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"  # Basic <base64 encoded client_id:client_secret>
        }

    def get_token_data(self):
        return {"grant_type": "client_credentials"}

    def perform_auth(self):
        """
        METHOD: Authenticate to Spotify by acquiring token
        """
        token_URL = self.token_URL
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()

        # Get Token Response
        response = requests.post(token_URL, data=token_data, headers=token_headers)

        # Exit if Request is Invalid...
        if response.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False

        # Else, proceed...
        token_response_data = response.json()

        access_token = token_response_data["access_token"]

        expires_in = token_response_data["expires_in"]  # Unit: Seconds
        now = datetime.datetime.now()
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now

        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires

        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers

    def get_resource(
        self, lookup_id, resource_type="artists", sub_resource_type="", version="v1"
    ):
        headers = self.get_resource_header()

        if sub_resource_type != "":
            endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}/{sub_resource_type}"
        else:
            endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"

        print(endpoint)

        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}

        return r.json()

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type="artists")

    def get_artist_albums(self, _id):
        return self.get_resource(
            _id, resource_type="artists", sub_resource_type="albums"
        )

    def get_album(self, _id):
        return self.get_resource(_id, resource_type="albums")

    def get_album_tracks(self, _id):
        return self.get_resource(
            _id, resource_type="albums", sub_resource_type="tracks"
        )

    def get_track(self, _id):
        return self.get_resource(_id, resource_type="tracks")

    def get_track_features(self, _id):
        return self.get_resource(_id, resource_type="audio-features")

    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        print(lookup_url)

        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}

        return r.json()

    def search(
        self, query=None, operator=None, operator_query=None, search_type="artist"
    ):
        if query == None:
            raise Exception("A query is required")

        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k, v in query.items()])

        if (operator != None) and (operator_query != None):
            if (operator.lower() == "or") or (operator.lower() == "not"):
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"

        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)
