import pvrhino
from pvrecorder import PvRecorder
import time

engineer = pvrhino.create(
    access_key="+8P7CZmuTTw2Ock1VclK1XskRBAJlQiouUISmeCqaMWQAxWiJ+Rw3w==",
    context_path="/home/EnginEar/Desktop/Proto_OS/EnginEar_en_raspberry-pi_v3_0_0.rhn"
)

def loop():
    recorder = PvRecorder(frame_length=512)
    recorder.start()

    hall = 1
    patriotism = 0
    with open("db.txt", "r") as fs:
        splited = fs.readline().split("\t")
        emotion = int(splited[0])
        fs.close()
    
    print("Recoding")
    try:
        while True:
            pcm = recorder.read()
            is_finalized = engineer.process(pcm)

            if is_finalized:
                inference = engineer.get_inference()
                if inference.is_understood:

                    with open("db.txt", "r") as fs:
                        splited = fs.readline().split("\t")
                        hall = eval(splited[1])
                        patriotism = eval(splited[2])
                        fs.close()
                    with open("db.txt", "w") as fs:
                        fs.write(f"7\t{hall}\t{patriotism}\t1")
                        fs.close()

                    slots = inference.slots
                    print("Slots:")
                    keys = list(slots.keys())
                    if "emotion" in keys:
                        try:
                            emotion = ["Default", "Happy", "Tired", "Close eyes", "Angry", "Furious", "Sad", "Questions", "Confused", "Love"].index(slots["emotion"])
                        except ValueError:
                            pass
                    elif "mode" in keys:
                        match slots["mode"]:
                            case "Make Hungary great again":
                                patriotism = 1
                            case "Default lights":
                                patriotism = 0

                    time.sleep(1.5)
                    with open("db.txt", "w") as fs:
                        fs.write(f"{emotion}\t{hall}\t{patriotism}\t1")
                        fs.close()

    except KeyboardInterrupt:
        pass
    finally:
        engineer.delete()
        recorder.delete()
        with open("db.txt", "w") as fs:
            fs.write(f"{emotion}\t{hall}\t{patriotism}\t1")
            fs.close()

if __name__ == "__main__":
    loop()