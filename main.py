import music_tag
import requests
import sys, base64
from pydub import AudioSegment
import json
from apikey import APIKey

def detect_raw_audio(bytestream, api_key):
	url = "https://shazam.p.rapidapi.com/songs/detect"

	headers = {
		"content-type": "text/plain",
		"X-RapidAPI-Key": api_key,
		"X-RapidAPI-Host": "shazam.p.rapidapi.com"
	}

	response = requests.request("POST", url, data=bytestream, headers=headers)

	#TODO this is broken if we don't get a match, harden this
	return json.loads(response.text)['matches'][0]['id']


def get_album_id_from_song_id(song_id, api_key):
	url = "https://shazam.p.rapidapi.com/songs/get-details"

	querystring = {"key": song_id, "locale": "en-US"}

	headers = {
		"X-RapidAPI-Key": api_key,
		"X-RapidAPI-Host": "shazam.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	# TODO this is broken if we don't get a match, harden this
	return json.loads(response.text)['albumadamid']

def get_album_details_from_album_id(album_id, api_key):
	url = "https://shazam.p.rapidapi.com/albums/get-details"

	querystring = {"id": album_id, "l": "en-US"}

	headers = {
		"X-RapidAPI-Key": api_key,
		"X-RapidAPI-Host": "shazam.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	# TODO this is broken if we don't get a match, harden this
	return json.loads(response.text)

song = AudioSegment.from_mp3("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3")
first_5_seconds = song[:5000]
first_5_seconds.export("new.mp3", format="mp3")
#todo preprocess cut file
#ffmpeg -i new.mp3 -ar 44100 -ac 1 -f s16le -acodec pcm_s16le mono4.raw

test_file = open("mono4.raw", 'rb')
# b = base64.b64decode((test_file.read()))
b = base64.b64encode(test_file.read())

api_key = APIKey()
key = api_key.api_key

song_id = detect_raw_audio(b, key)
album_id = get_album_id_from_song_id(song_id, key)
album_details = get_album_details_from_album_id(album_id, key)
x = 4

# print(response.text)
# hit detect api with raw audio encoded
# hit get info api with detection ID
# hit album api with album ID, get artwork, artist, album title, date, etc.

# ffmpeg -i new.mp3 -ar 44100 -ac 1 mono4.flac

# test_mp3 = open("new.mp3", 'r')
# b = base64.b64decode((test_mp3.read()))
x = 4

# test_mp3 = open("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3", 'r')
# b = base64.b64decode(test_mp3.read())
# file = music_tag.load_file("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3")
# file['albumartist'] = "test2"
# file['artist'] = "test"
# file.save()