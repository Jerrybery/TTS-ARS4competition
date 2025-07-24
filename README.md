本文档旨在快速帮助你使用这个基于`paddlespeech`的流式tts/asr项目。下面是如何配置此环境的教程：

# 必要系统依赖
主要是`libportaudio2`和`mpv`
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
python -m pip install paddlepaddle-gpu==3.1.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
pip uninstall aistudio-sdk
pip install aistudio-sdk==0.2.6

# 如果你是Ubuntu 20.4及以下，只要你的系统不支持gcc12的，请运行以下命令：
pip uninstall opencc
pip install opencc==1.1.6
# 换为你当前系统支持的版本即可
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

使用ASR时请先启动`server.py`和`client.py`，然后通过`recorder.py`中的函数采集音频。