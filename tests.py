import time

global INTQ
INTQ = False
class Animation:
    mouth_sync_ena = True
    emotions = ("Default","Happy","Tired","Eyes-closed","Angry","Furious","Confiused","Thinking","Inquestitive", "Love")
    emotion_id = 0
    patroitism = False

    def __init__(self):
        print("Initializer functions: ON")

    def write_interrupt(self):
        INTQ = True
        fp = open("db.txt")
        splited = fp.readline().split("\t")
        self.emotion_id = int(splited[0])
        self.mouth_sync_ena = bool(splited[1])
        self.patroitism = bool(splited[2])
        INTQ = False
        return
        

    def loop(self):
        if self.mouth_sync_ena:
            print("Lip sync enabled")
        else:
            print("Lip sync disabled")
        print("Blink")
        print("Emotion:", self.emotions[self.emotion_id])


ani = Animation()

if __name__ == "__main__":
    while True:
        while not INTQ:
            ani.loop()
        ani.write_interrupt()