from paddlespeech.server.bin.paddlespeech_server import ServerExecutor # ASR server
import paddle
import sys
import wave

if __name__ == "__main__":
    server_ASR_executor = ServerExecutor()  
    server_ASR_executor(config_file="cfg/ws_conformer_application.yaml")