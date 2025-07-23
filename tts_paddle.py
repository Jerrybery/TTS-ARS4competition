import sounddevice as sd  # 需要安装：pip install sounddevice
import numpy as np
from paddlespeech.cli.tts import TTSExecutor
import os

class AgentSpeaker():
    def __init__(self):
        self.model = TTSExecutor()

    def __call__(self, text):
        audio_data = self.model(text=text, output="temp.wav")
        with open("TTS_ASR/temp.wav", "rb") as f:
            audio_data = np.frombuffer(f.read(), dtype=np.int16)
        sd.play(audio_data, samplerate=24000) # 直接播放
        sd.wait()
        os.remove("TTS_ASR/temp.wav")

if __name__ == "__main__":
    speaker = AgentSpeaker()
    speaker("求你了，别炸我了")