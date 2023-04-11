import os
import music_tag
import eyed3
from eyed3.id3.frames import ImageFrame

def music_file_with_missing_attributes(filepath):
    if os.path.splitext(filepath)[1] != '.mp3':
        return False

    file = music_tag.load_file(filepath)
    for key in ["title", "artist", "albumartist", "album", "genre", "year", "tracknumber"]:
    # for key in ["year"]:
        if not field_is_valid(file[key]):
            return True
    return False


def field_is_valid(metadata_item):
    if type(metadata_item.value) == int:
        #todo this check isn't correct
        return True
    return len(metadata_item.value) > 0


def find_candidate_files(path, filter_fcn=music_file_with_missing_attributes):
    for root, dirs, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)
            if filter_fcn(full_path):
                yield full_path


def write_file_metadata(filepath, song_details, album_details):

    file = music_tag.load_file(filepath)
    file['artist'] = album_details['data'][0]['attributes']['artistName']
    file['albumartist'] = album_details['data'][0]['attributes']['artistName']
    file['title'] = song_details['title']
    file['album'] = album_details['data'][0]['attributes']['name']
    file['genre'] = song_details['genres']['primary']
    file.raw['tracknumber'] = retrieve_track_number(song_details['title'], album_details)
    # file.raw['year'] = album_details['data'][0]['attributes']['releaseDate'][0:4]
    file['year'] = int(album_details['data'][0]['attributes']['releaseDate'][0:4])
    # f = eyed3.load(filepath)
    # f.initTag()
    # f.tag.year = int(album_details['data'][0]['attributes']['releaseDate'][0:4])
    # f.tag.save()
    # time.sleep(5)
    #year field is written but only displays when we view it first in the debugger
    # _ = file['year']
    file.save()


def retrieve_track_number(song_title, album_details):
    song_list = album_details['data'][0]['relationships']['tracks']['data']

    res = -1
    for idx, song in enumerate(song_list):
        if song['attributes']['name'] == song_title:
            res = idx + 1
            break

    if res < 10:
        return '0' + str(res)
    return str(res)


def rename_file(filepath, song_details):
    working_dir = os.path.dirname(filepath)
    if not os.path.exists(os.path.join(working_dir, song_details['title'] + '.mp3')):
        os.rename(filepath, os.path.join(working_dir, song_details['title'] + '.mp3'))


def add_album_artwork(filepath):

    base_name = os.path.basename(filepath)
    base_name_no_ext = base_name[:base_name.rindex('.')]
    dir_name = os.path.dirname(filepath)
    jpg_path = os.path.join(dir_name, base_name_no_ext + '.jpg')

    audio_file = eyed3.load(filepath)
    if audio_file.tag is None:
        audio_file.initTag()

    audio_file.tag.images.set(ImageFrame.FRONT_COVER, open(jpg_path, 'rb').read(), 'image/jpeg')
    audio_file.tag.save(version=eyed3.id3.ID3_V2_3)


def cleanup_raw_files():
    curr_dir = os.path.dirname(os.path.realpath(__file__))

    for root, dirs, files in os.walk(curr_dir):
        for filename in files:
            if filename.endswith('.raw'):
                os.remove(os.path.join(curr_dir, filename))


def cleanup_jpg_files(working_dir):
    for root, dirs, files in os.walk(working_dir):
        for filename in files:
            if filename.endswith('.jpg'):
                os.remove(os.path.join(root, filename))
