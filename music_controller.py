
from pygame import mixer
import constants as c

class MusicController():
    def __init__(self):
        mixer.init()
        self.bg_channel = mixer.Channel(0)
        self.bg_channel.set_volume(0.7)
        self.fx_channel = mixer.Channel(1)

    def start(self):
        self.bg_channel.play(c.SND_BG, loops=-1)

    def stop(self):
        self.bg_channel.stop()

    def play_move_sound(self):
        self.fx_channel.play(c.SND_MOVE)
    
    def play_select_sound(self):
        self.fx_channel.play(c.SND_SELECT)