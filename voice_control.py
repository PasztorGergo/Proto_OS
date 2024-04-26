from whisper_live.server import TranscriptionServer
import os

os.environ["KMP_DUPLICATE_LIB_OK"]="True"
server = TranscriptionServer()
server.run("0.0.0.0", port=9090)