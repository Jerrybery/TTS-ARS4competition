from paddlespeech.server.bin.paddlespeech_client import ASROnlineClientExecutor
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import asyncio

asrclient_executor = ASROnlineClientExecutor()

class WavHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".wav"):
            print(f"检测到新音频文件: {event.src_path}")
            try:
                asyncio.set_event_loop(asyncio.new_event_loop())
                res = asrclient_executor(
                    input=event.src_path,
                    server_ip="127.0.0.1",
                    port=8090,
                    sample_rate=16000,
                    lang="zh_cn",
                    audio_format="wav",
                )
                print("ASR processing finished")
                result_path = "paddleASR/detection_result.json"
                # 读取已有 json
                if os.path.exists(result_path):
                    try:
                        with open(result_path, "r", encoding="utf-8") as f:
                            result_dic = json.load(f)
                        print("file exist")
                    except Exception:
                        result_dic = {}
                        print("JSON文件为空或格式错误，已重置为空字典")
                else:
                    result_dic = {}
                # 编号
                idx = f"prompt_{len(result_dic)}"
                # 从文件名中提取时间
                filename = os.path.basename(event.src_path)
                time_str = filename.replace("sound_", "").replace(".wav", "")
                result_dic[idx] = {
                    "text": res,
                    "file_time": time_str,
                }
                print("result in dic")
                # 保存
                with open(result_path, "w", encoding="utf-8") as f:
                    json.dump(result_dic, f, ensure_ascii=False, indent=4)
                print("result saved")
            except Exception as e:
                print(f"Error: {e}")
        # delect the file after processing
        os.remove(event.src_path)
        print(f"已删除音频文件: {event.src_path}")
        print("等待下一个音频文件...")

if __name__ == "__main__":
    # 确保音频目录存在
    os.makedirs("paddleASR/audio", exist_ok=True)
    
    # 监听音频目录
    event_handler = WavHandler()
    observer = Observer()
    observer.schedule(event_handler, path="paddleASR/audio", recursive=False)
    observer.start()
    
    try:
        print("开始监听音频文件...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


