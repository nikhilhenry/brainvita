
from pygame import mixer
import constants as c

class MusicController():
    def __init__(self):
        mixer.init()
        self.bg_channel = mixer.Channel(0)

    def start(self):
        self.bg_channel.play(c.SND_BG, loops=-1)

    def stop(self):
        self.bg_channel.stop()