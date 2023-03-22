import music_tag
import subprocess
import requests
import base64
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
	return json.loads(response.text)


def get_details_from_song_id(song_id, api_key):
	url = "https://shazam.p.rapidapi.com/songs/get-details"

	querystring = {"key": song_id, "locale": "en-US"}

	headers = {
		"X-RapidAPI-Key": api_key,
		"X-RapidAPI-Host": "shazam.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	return json.loads(response.text)


def get_album_id_from_song_id(song_id, api_key):
	url = "https://shazam.p.rapidapi.com/songs/get-details"

	querystring = {"key": song_id, "locale": "en-US"}

	headers = {
		"X-RapidAPI-Key": api_key,
		"X-RapidAPI-Host": "shazam.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	# TODO this is broken if we don't get a match, harden this
	return json.loads(response.text)

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


def bytestream_from_unknown_mp3(mp3_path, filename):
	# TODO need to block on this call so that we ensure the trimmed mp3 is present for processing by ffmpeg
	full_song = AudioSegment.from_mp3(mp3_path)
	first_5_seconds = full_song[:5000]
	first_5_seconds.export(filename + 'trimmed.mp3')
	conversion = subprocess.call('ffmpeg -i ' + filename + 'trimmed.mp3 -ar 44100 -ac 1 -f s16le -acodec pcm_s16le' + filename + 'trimmed.raw')
	raw_file = open(filename + 'trimmed.raw', 'rb')
	return base64.b64encode(raw_file.read())


api_key = APIKey()
key = api_key.api_key

b = bytestream_from_unknown_mp3("C:\\Users\\bennu\\OneDrive\\Desktop\\test2.mp3", 'test2')
song_id = detect_raw_audio(b, key)['matches'][0]['id']
song_details = get_details_from_song_id(song_id, key)
album_id = get_album_id_from_song_id(song_id, key)['albumadamid']
album_details = get_album_details_from_album_id(album_id, key)
x = 4


# file = music_tag.load_file("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3")
# file['albumartist'] = "test2"
# file['artist'] = "test"
# file.save()