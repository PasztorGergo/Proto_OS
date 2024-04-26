from whisper_live.client import TranscriptionClient

client = TranscriptionClient(host="localhost", port=9090, model_size="small", lang="en")

client()