import music_tag

file = music_tag.load_file("C:\\Users\\bennu\\OneDrive\\Desktop\\testbed.mp3")
file['albumartist'] = "test2"
file['artist'] = "test"
file.save()