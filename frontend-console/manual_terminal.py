import subprocess
import sys
sys.path.insert(0, '../calculator')

from speaker_id import AudioConverter

audio_converter = AudioConverter()
audio_hex = audio_converter.wav_to_hex('../calculator/data_test/test2_speaker2.wav')
print(type(audio_hex))
print(sys.getsizeof(audio_hex) / 1024)

# subprocess.run(["ls", "-l"])
subprocess.run(["/usr/local/bin/yarn", "start", 'input', 'send', "--payload", "ffff"], shell=True)
