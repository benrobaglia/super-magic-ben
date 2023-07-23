from os import environ
import os
import sys
import wave
import numpy as np
import json
import binascii
import io
from vosk import Model, KaldiRecognizer, SpkModel

from pydub import AudioSegment


def convert_flac_to_mono_wav(flac_file):
    audio = AudioSegment.from_file(flac_file, format="flac")

    # set the audio to mono
    mono_audio = audio.set_channels(1)
    
    wav_file = flac_file.replace(".flac", ".wav")
    mono_audio.export(wav_file, format="wav")
    return wav_file


def write_bytes_to_file(bytes_data, file_path):
    with open(file_path, 'wb') as file:
        file.write(bytes_data)


# Inputs: .wav file in mono PCM format, speaker id

class SpeakerId:
    def __init__(self):
        self.speaker_dic = {}
        self.SPK_MODEL_PATH = "vosk-model-spk-0.4"

        if not os.path.exists(self.SPK_MODEL_PATH):
            print("Please download the speaker model from "
                "https://alphacephei.com/vosk/models and unpack as {SPK_MODEL_PATH} "
                "in the current folder.")
            sys.exit(1)
    
    def cosine_dist(self, x, y):
        nx = np.array(x)
        ny = np.array(y)
        return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

    def reject(self, x):
        if x < 0.5:
            return 1
        else: 
            return 0

    def create_speaker(self, new_footprint, new_speaker_id):
        wf = wave.open(new_footprint, "rb")

        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            sys.exit(1)
        model = Model(lang="en-us")
        spk_model = SpkModel(self.SPK_MODEL_PATH)
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetSpkModel(spk_model)

        while True:
            data = wf.readframes(40000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())

        res = json.loads(rec.FinalResult())
        
        if "spk" in res:
            self.speaker_dic[new_speaker_id] = res['spk']
            print('Speaker voice footprint successfully created!')
        
        return res["text"]
    
    def verify_speaker(self, audio_to_test, claimed_speaker):
        wf = wave.open(audio_to_test, "rb")

        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            sys.exit(1)
        model = Model(lang="en-us")
        spk_model = SpkModel(self.SPK_MODEL_PATH)
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetSpkModel(spk_model)

        spk_sig = self.speaker_dic[claimed_speaker]

        while True:
            data = wf.readframes(40000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())

        res = json.loads(rec.FinalResult())        
        print("Text:", res["text"])
        speaker_dis =  (self.cosine_dist(spk_sig, res["spk"]))
        if "spk" in res:
            return [speaker_dis,  self.reject(speaker_dis)]    
        


class AudioConverter:
    def __init__(self, num_channels=1, sample_width=2, frame_rate=16000):
        # num_channels = 1  # Mono
        # sample_width = 2  # 2 bytes per sample (16-bit)

        self.num_channels = num_channels
        self.sample_width = sample_width
        self.frame_rate = frame_rate

    ############ helper function ###########
    def wav_to_hex(self, filename):
        with open(filename, 'rb') as f:
            content = f.read()
        return binascii.hexlify(content)

    
    # def hex_to_wav(self, hex_string, output_file_path):
    #     wav_buffer = io.BytesIO()

    #     try:
    #         # Convert hexadecimal string to binary data
    #         binary_data = binascii.unhexlify(hex_string)
            
    #         # Set the WAV file parameters (you may need to adjust these based on your specific case)
    #         num_frames = len(binary_data) // (self.num_channels * self.sample_width)
            
    #         # Open the WAV file for writing
    #         with wave.open(wav_buffer, 'wb') as wav_file:
    #             wav_file.setnchannels(self.num_channels)
    #             wav_file.setsampwidth(self.sample_width)
    #             wav_file.setframerate(self.frame_rate)
    #             wav_file.setnframes(num_frames)
                
    #             # Write the binary data to the WAV file
    #             wav_file.writeframes(binary_data)
    #             return wav_file
    #         print(f"Successfully converted hexadecimal data to WAV ")
    #     except Exception as e:
    #         print(f"Error occurred: {str(e)}")

    def hex_to_wav(self, hex_string, output_file_path):
        try:
            # Convert hexadecimal string to binary data
            binary_data = binascii.unhexlify(hex_string)

            # Set the WAV file parameters (you may need to adjust these based on your specific case)
            num_frames = len(binary_data) // (self.num_channels * self.sample_width)

            # Open the WAV file for writing
            with wave.open(output_file_path, 'wb') as wav_file:
                wav_file.setnchannels(self.num_channels)
                wav_file.setsampwidth(self.sample_width)
                wav_file.setframerate(self.frame_rate)
                wav_file.setnframes(num_frames)

                # Write the binary data to the WAV file
                wav_file.writeframes(binary_data)
        except binascii.Error as e:
            print(f"Error during hexadecimal conversion: {str(e)}")
            return None
        except wave.Error as e:
            print(f"Error during WAV file writing: {str(e)}")
            return None
