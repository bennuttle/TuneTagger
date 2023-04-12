import os.path

import pydub.exceptions
import requests

from shazammanager import ShazamManager
from audiomanager import bytestream_from_unknown_mp3
from filemanager import find_candidate_files, write_file_metadata, rename_file, cleanup_raw_files, add_album_artwork, cleanup_jpg_files, move_problem_file, makedir_if_absent, reorganize_files


CLEANUP_DIRECTORY = "C:\\Users\\bennu\\OneDrive\\Desktop\\chelsea_phone_test"
BAD_FILES_DIRNAME = "TuneTagger_BadFiles"
bad_files_directory = os.path.join(CLEANUP_DIRECTORY, BAD_FILES_DIRNAME)
makedir_if_absent(CLEANUP_DIRECTORY, bad_files_directory)

sm = ShazamManager()
for filepath in find_candidate_files(CLEANUP_DIRECTORY, BAD_FILES_DIRNAME):
    try:
        b = bytestream_from_unknown_mp3(filepath)
        song_id = sm.detect_raw_audio(b)['matches'][0]['id']
        song_details = sm.get_details_from_song_id(song_id)
        album_id = song_details['albumadamid']
        album_details = sm.get_album_details_from_album_id(album_id)

        sm.get_album_artwork(filepath, song_details)
        write_file_metadata(filepath, song_details, album_details)
        add_album_artwork(filepath)
        rename_file(filepath, song_details)
    except requests.HTTPError:
        print("Bad API response when processing " + filepath + ". Continuing..")
        move_problem_file(filepath, bad_files_directory)
        continue
    except KeyError:
        print("Incomplete Metadata for " + filepath + ". Continuing..")
        move_problem_file(filepath, bad_files_directory)
        continue
    except IndexError:
        # we had no matches from shazam API so we get a key error when trying to ID the song on ln 15
        print("??? " + filepath + ". Continuing..")
        move_problem_file(filepath, bad_files_directory)
        continue
    except FileNotFoundError:
        print("Bad path? " + filepath + ". Continuing..")
        move_problem_file(filepath, bad_files_directory)
        continue
    except pydub.exceptions.CouldntDecodeError:
        # might be fixed by the code change to from_file??
        print("WTF mate?")
        move_problem_file(filepath, bad_files_directory)
        continue

cleanup_raw_files()
cleanup_jpg_files(CLEANUP_DIRECTORY)
reorganize_files(CLEANUP_DIRECTORY, bad_files_directory)


