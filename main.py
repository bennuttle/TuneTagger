import music_tag
import requests
import sys, base64
from pydub import AudioSegment

song = AudioSegment.from_mp3("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3")
first_5_seconds = song[:5000]
first_5_seconds.export("new.mp3", format="mp3")

# test_mp3 = open("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3", 'r')
# b = base64.b64decode(test_mp3.read())
# x = 4
# file = music_tag.load_file("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3")
# file['albumartist'] = "test2"
# file['artist'] = "test"
# file.save()

# import requests
#
# url = "https://shazam.p.rapidapi.com/search"
#
# querystring = {"term":"kiss the rain","locale":"en-US","offset":"0","limit":"5"}
#
# headers = {
# 	"X-RapidAPI-Key": "cfa32d36e2mshe97309c0391759ep1baffdjsn896925dac04e",
# 	"X-RapidAPI-Host": "shazam.p.rapidapi.com"
# }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
#
# print(response.text)



# url = "https://shazam.p.rapidapi.com/songs/detect"
#
# payload = "\"Generate one on your own for testing and send the body with the content-type as text/plain\""
# headers = {
# 	"content-type": "text/plain",
# 	"X-RapidAPI-Key": "cfa32d36e2mshe97309c0391759ep1baffdjsn896925dac04e",
# 	"X-RapidAPI-Host": "shazam.p.rapidapi.com"
# }
#
# response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
