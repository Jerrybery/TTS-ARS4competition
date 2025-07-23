本文档旨在快速帮助你使用这个基于`paddleSpeech`的流式tts/asr项目。

# 必要系统依赖
1. `libportaudio2`和`mpv`
通过如命令即可安装（Ubuntu）
```bash
sudo apt-get update
sudo apt-get install libportaudio2 mpv
```

# 配置conda环境
首先创建环境
```bash
conda env create -f enviornment.yml
conda activate StreamingSpeech
```
然后通过pip下载需要的包
```bash
pip install -r requirements.txt
```
为保证你能够正常使用这个仓库，建议使用本地安装的方式下载`paddlespeech`此库，即：
```bash
git clone https://github.com/PaddlePaddle/PaddleSpeech.git /path/to/PaddleSpeech
cd /path/to/paddleSpeech && pip install -e . --use-pep517
```

# 使用
## 文件说明
| 文件              | 功能                                                                 | 使用                 |
| --------------- | ------------------------------------------------------------------ | ------------------ |
| `client.py`     | 监察`audio`下的`.wav`文件，提交至服务器转文字，存储在`detection_result.json`中，并且删除录音文件 | `python client.py` |
| `server.py`     | 提供ASR服务                                                            | `python server.py` |
| `tts_paddle.py` | 包含`AgentSpeaker`类，用于文字转语音                                          | 略                  |
| `recorder.py`   | 包含录音函数，使用函数时会检测静音情况下的声音强度，在静音时长超过1.5s后停止录音并存储到`audio`下             | 略                  |
运行ASR服务会创建文件`detection_result.json`，其格式为：
```JavaScript
{
	"prompt_0":{
		"text": "这是一段测试音频"，
		"file_time": "2025-07-23 11:45:14"
	}
}
```