import os
from pydub import AudioSegment
import base64


def bytestream_from_unknown_mp3(mp3_path):
    base_name = os.path.basename(mp3_path)
    base_name_no_ext = base_name[:base_name.rindex('.')]

    full_song = AudioSegment.from_file(mp3_path)
    #todo determine song length and cut into the middle? Luke Brian Song tagged incorrectly
    midsong_start_ms = full_song.duration_seconds * 1000 // 2
    midsong_end_ms = midsong_start_ms + 5000
    sample_5_seconds = full_song[midsong_start_ms:midsong_end_ms]

    extra_params = ["-ar", "44100", "-ac", "1"]
    sample_5_seconds.export(base_name_no_ext + '.raw', format='s16le', codec='pcm_s16le', parameters=extra_params)

    raw_file = open(base_name_no_ext + '.raw', 'rb')
    return base64.b64encode(raw_file.read())

