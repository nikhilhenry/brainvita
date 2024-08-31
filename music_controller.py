from pygame import mixer
import constants as c


class MusicController:
    def __init__(self, bg_volume: int = 0.6, fx_volume: int = 1):
        mixer.init()

        self.bg_volume = bg_volume
        self.fx_volume = fx_volume

        self.bg_channel = mixer.Channel(0)
        self.bg_channel.set_volume(self.bg_volume)
        self.fx_channel = mixer.Channel(1)
        self.fx_channel.set_volume(self.fx_volume)

        self.is_playing = True

    def start(self):
        self.bg_channel.play(c.SND_BG, loops=-1)

    def play_move_sound(self):
        self.fx_channel.play(c.SND_MOVE)

    def play_select_sound(self):
        self.fx_channel.play(c.SND_SELECT)

    def mute(self):
        self.is_playing = False
        self.bg_channel.set_volume(0)
        self.fx_channel.set_volume(0)

    def unmute(self):
        self.is_playing = True
        self.bg_channel.set_volume(self.bg_volume)
        self.fx_channel.set_volume(self.fx_volume)
