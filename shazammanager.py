from apikey import APIKey
import requests
from pydub import AudioSegment
import json
import base64
import subprocess


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

        # TODO this is broken if we don't get a match, harden this
        return json.loads(response.text)

    def post_to_api(self, endpoint_url, data):
        response = requests.request("POST", endpoint_url, data=data, headers=self.headers_post)

        # TODO this is broken if we don't get a match, harden this
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

    def bytestream_from_unknown_mp3(self, mp3_path, filename):
        # TODO need to block on this call so that we ensure the trimmed mp3 is present for processing by ffmpeg
        full_song = AudioSegment.from_mp3(mp3_path)
        first_5_seconds = full_song[:5000]
        first_5_seconds.export(filename + 'trimmed.mp3')
        conversion = subprocess.call(
            'ffmpeg -i ' + filename + 'trimmed.mp3 -ar 44100 -ac 1 -f s16le -acodec pcm_s16le' + filename + 'trimmed.raw')
        raw_file = open(filename + 'trimmed.raw', 'rb')
        return base64.b64encode(raw_file.read())