import os.path

from apikey import APIKey
import requests
import json


class ShazamManager:

    def __init__(self):

        key = APIKey().api_key

        self.headers_get = {
            "X-RapidAPI-Key": key,
            "X-RapidAPI-Host": "shazam.p.rapidapi.com"
        }

        self.headers_post = {
            "content-type": "text/plain",
            "X-RapidAPI-Key": key,
            "X-RapidAPI-Host": "shazam.p.rapidapi.com"
        }

    def get_from_api(self, endpoint_url, querystring):
        response = requests.request("GET", endpoint_url, headers=self.headers_get, params=querystring)

        response.raise_for_status()
        return json.loads(response.text)

    def post_to_api(self, endpoint_url, data):
        response = requests.request("POST", endpoint_url, data=data, headers=self.headers_post)

        response.raise_for_status()
        return json.loads(response.text)

    def detect_raw_audio(self, bytestream):
        url = "https://shazam.p.rapidapi.com/songs/detect"

        return self.post_to_api(url, bytestream)

    def get_details_from_song_id(self, song_id):
        url = "https://shazam.p.rapidapi.com/songs/get-details"
        querystring = {"key": song_id, "locale": "en-US"}

        return self.get_from_api(url, querystring)

    def get_album_details_from_album_id(self, album_id):
        url = "https://shazam.p.rapidapi.com/albums/get-details"
        querystring = {"id": album_id, "l": "en-US"}

        return self.get_from_api(url, querystring)

    @staticmethod
    def get_album_artwork(filepath, song_details):
        img_url = song_details['images']['coverart']
        base_name = os.path.basename(filepath)
        base_name_no_ext = base_name[:base_name.rindex('.')]
        dir_name = os.path.dirname(filepath)

        jpg_path = os.path.join(dir_name, base_name_no_ext + '.jpg')

        img_data = requests.get(img_url).content
        with open(jpg_path, 'wb') as handler:
            handler.write(img_data)
