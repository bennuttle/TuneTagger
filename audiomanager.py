import os
from pydub import AudioSegment
import base64


def bytestream_from_unknown_mp3(mp3_path):
    base_name = os.path.basename(mp3_path)
    base_name_no_ext = base_name[:base_name.rindex('.')]

    full_song = AudioSegment.from_mp3(mp3_path)
    first_5_seconds = full_song[:5000]

    extra_params = ["-ar", "44100", "-ac", "1"]
    first_5_seconds.export(base_name_no_ext + '.raw', format='s16le', codec='pcm_s16le', parameters=extra_params)

    raw_file = open(base_name_no_ext + '.raw', 'rb')
    return base64.b64encode(raw_file.read())

