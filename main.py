import music_tag
import requests
import sys, base64
from pydub import AudioSegment

song = AudioSegment.from_mp3("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3")
first_5_seconds = song[:5000]
first_5_seconds.export("new.mp3", format="mp3")

test_mp3 = open("new.mp3", 'r')
b = base64.b64decode((test_mp3.read()))

x = 4

# test_mp3 = open("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3", 'r')
# b = base64.b64decode(test_mp3.read())
# x = 4
# file = music_tag.load_file("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3")
# file['albumartist'] = "test2"
# file['artist'] = "test"
# file.save()
