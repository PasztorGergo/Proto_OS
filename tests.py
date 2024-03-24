import time

class Animation:
    mouth_sync_ena = True
    emotions = ("Default","Happy","Tired","Eyes-closed","Angry","Furious","Confiused","Thinking","Inquestitive", "Love")
    emotion_id = 0
    data = []

    def __init__(self):
        print("Initializer functions: ON")

    def loop(self):
        fp = open("db.txt")
        splited = fp.readline().split("\t")
        self.emotion_id = int(splited[0])
        self.mouth_sync_ena = bool(splited[1])

        if self.mouth_sync_ena:
            print("Lip sync enabled")
        else:
            print("Lip sync disabled")
        time.sleep(2)
        print("Blink")
        print("Emotion:", self.emotions[self.emotion_id])


ani = Animation()

if __name__ == "__main__":
    while True:
        ani.loop()