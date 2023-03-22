import os
import music_tag

# file = music_tag.load_file("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3")
# file['albumartist'] = "test2"
# file['artist'] = "test"
# file.save()

# delete all raw files in directory for cleanup
# methods to write fields given the results dicts from shazam
#maybe one for album artwork? would be cool


def music_file_with_missing_attributes(filepath):
    if os.path.splitext(filepath)[1] != '.mp3':
        return False

    file = music_tag.load_file(filepath)
    for key in ["artist", "albumartist", "album"]:
        if not field_is_valid(file[key]):
            return True
    return False


def field_is_valid(metadata_item):
    return len(metadata_item.value) > 0


def find_candidate_files(path, filter_fcn=music_file_with_missing_attributes):
    for root, dirs, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)
            if filter_fcn(full_path):
                yield full_path

