import sounddevice as sd
import numpy as np
import wave
import time
import os

SAMPLE_RATE = 16000
CHANNELS = 1
SILENCE_THRESHOLD = 1.5  # 静音多少秒后停止
SILENCE_DURATION = 0.1  # 前100ms采样静音能量
ENERGY_OFFSET = 14000     # 阈值偏移量

def record_until_silence():
    buffer = []
    recording = False
    last_voice_time = None
    silence_energy = []
    output_file = f"paddleASR/audio/sound_{time.strftime('%Y-%m-%d %H:%M:%S')}.wav"

    def silence_callback(indata, frames, cb_time, status):
        nonlocal silence_energy
        energy = np.sum(indata.astype(np.float32) ** 2) / len(indata)
        silence_energy.append(energy)

    print("采集静音能量基线...")
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        callback=silence_callback
    ):
        time.sleep(SILENCE_DURATION)
    base_energy = np.mean(silence_energy)
    ENERGY_THRESHOLD = base_energy + ENERGY_OFFSET
    print(f"静音能量均值: {base_energy:.2f}, 阈值设为: {ENERGY_THRESHOLD:.2f}")

    def callback(indata, frames, cb_time, status):
        nonlocal buffer, recording, last_voice_time
        energy = np.sum(indata.astype(np.float32) ** 2) / len(indata)
        # print(energy)
        if energy > ENERGY_THRESHOLD:
            if not recording:
                print("🎤 检测到人声，开始录音...")
                recording = True
            last_voice_time = time.time()
            buffer.append(indata.copy())
        elif recording:
            buffer.append(indata.copy())

    print("等待人声输入...")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        callback=callback
    ):
        while True:
            if recording and last_voice_time is not None:
                current_time = time.time()
                if current_time - last_voice_time > SILENCE_THRESHOLD:
                    print("🔇 检测到静音，停止录音")
                    break
            time.sleep(0.1)

    if buffer:
        audio_data = np.concatenate(buffer)
        with wave.open(output_file, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_data.tobytes())
        print(f"✅ 录音已保存至 {output_file}")
    else:
        print("❌ 未检测到语音，未保存文件")

if __name__ == "__main__":
    record_until_silence()
