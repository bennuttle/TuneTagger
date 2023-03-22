import music_tag
from shazammanager import ShazamManager
from audiomanager import bytestream_from_unknown_mp3


sm = ShazamManager()
b = bytestream_from_unknown_mp3("C:\\Users\\bennu\\OneDrive\\Desktop\\test2.mp3")
song_id = sm.detect_raw_audio(b)['matches'][0]['id']
song_details = sm.get_details_from_song_id(song_id)
album_id = song_details['albumadamid']
album_details = sm.get_album_details_from_album_id(album_id)
x = 4


# file = music_tag.load_file("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3")
# file['albumartist'] = "test2"
# file['artist'] = "test"
# file.save()