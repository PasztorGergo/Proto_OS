from faster_whisper import WhisperModel
import wave
import pyaudio
import os
import time
os.environ["KMP_DUPLICATE_LIB_OK"]="True"


def transcribe_chunk(chunk_file, model):
    segments, _ = model.transcribe(chunk_file, language="en", beam_size=7)
    transcription = ' '.join(segment.text for segment in segments)
    return transcription

def record_chunk(p, stream, file_path, chunk_length=1):
    frames = []
    for _ in range(0, int(16000/1024 * chunk_length)):
        data = stream.read(1024)
        frames.append(data)

    wf = wave.open(file_path, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()

def main2():
    model_size = "tiny.en"
    model = WhisperModel(model_size,compute_type="int8",device="cpu")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    silent_lines = 0
    listening = False
    hall = 1
    patriotism = 0
    with open("db.txt", "r") as fs:
        splited = fs.readline().split("\t")
        emotion = int(splited[0])
        fs.close()
    try:
        while True:
            chunk_file = "temp_chunk.wav"
            print("Recoding\n")
            record_chunk(p, stream, chunk_file,3)
            transcription = transcribe_chunk(chunk_file, model)
            print(transcription)
            if("engineer" in transcription.lower()):
                silent_lines = 0
                listening = True
                with open("db.txt", "r") as fs:
                    splited = fs.readline().split("\t")
                    hall = eval(splited[1])
                    patriotism = eval(splited[2])
                    fs.close()
                with open("db.txt", "w") as fs:
                    fs.write(f"7\t{hall}\t{patriotism}\t1")
                    fs.close()
            else:
                if listening:
                    word = transcription.split(" ")[1].lower().replace("!", "").replace(".", "").replace("?", "").replace(",", "")
                    print("\n", word)
                    try:
                        emotion = ["default", "happy", "tired", "eyes-closed", "angry", "furious", "said", "question mark", "confused", "love"].index(word)
                        with open("db.txt", "w") as fs:
                            fs.write(f"{emotion}\t{hall}\t{patriotism}\t1")
                            fs.close()
                    except ValueError:
                        pass

                else:
                    silent_lines += 1
                listening = False

            if silent_lines > 2:
                listening = False
                with open("db.txt", "r") as fs:
                    splited = fs.readline().split("\t")
                    hall = eval(splited[1])
                    patriotism = eval(splited[2])
                    fs.close()
                with open("db.txt", "w") as fs:
                    fs.write(f"{emotion}\t{hall}\t{patriotism}\t1")
                    fs.close()
            
            print("Translated")
            os.remove(chunk_file)
            time.sleep(0.025)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        silent_lines = 0
        listening = False
        with open("db.txt", "w") as fs:
            fs.write(f"{emotion}\t{hall}\t{patriotism}\t1")
            fs.close()

if __name__ == "__main__":
    main2()