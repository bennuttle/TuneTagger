from shazammanager import ShazamManager
from audiomanager import bytestream_from_unknown_mp3
from filemanager import find_candidate_files, write_file_metadata, rename_file, cleanup_raw_files


sm = ShazamManager()

for filepath in find_candidate_files("C:\\Users\\bennu\\OneDrive\\Desktop\\test_dir"):
    b = bytestream_from_unknown_mp3(filepath)
    song_id = sm.detect_raw_audio(b)['matches'][0]['id']
    song_details = sm.get_details_from_song_id(song_id)
    album_id = song_details['albumadamid']
    album_details = sm.get_album_details_from_album_id(album_id)

    sm.get_album_artwork(filepath, song_details)
    # write_file_metadata(filepath, song_details, album_details)
    # rename_file(filepath, song_details)

cleanup_raw_files()


