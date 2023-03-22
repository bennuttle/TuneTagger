import music_tag
import subprocess
import requests
import base64
from pydub import AudioSegment
import json
from apikey import APIKey
from shazammanager import ShazamManager




api_key = APIKey()
key = api_key.api_key

# b = bytestream_from_unknown_mp3("C:\\Users\\bennu\\OneDrive\\Desktop\\test2.mp3", 'test2')
# song_id = detect_raw_audio(b, key)['matches'][0]['id']
# song_details = get_details_from_song_id(song_id, key)
# album_id = get_album_id_from_song_id(song_id, key)['albumadamid']
# album_details = get_album_details_from_album_id(album_id, key)

sm = ShazamManager()

b = sm.bytestream_from_unknown_mp3("C:\\Users\\bennu\\OneDrive\\Desktop\\test2.mp3", 'test2')
song_id = sm.detect_raw_audio(b)['matches'][0]['id']
song_details = sm.get_details_from_song_id(song_id)
album_id = song_details['albumadamid']
album_details = sm.get_album_details_from_album_id(album_id)
x = 4


# file = music_tag.load_file("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3")
# file['albumartist'] = "test2"
# file['artist'] = "test"
# file.save()