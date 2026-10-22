"""Small original synthesised sound palette. Audio failure never prevents play."""
from array import array
import math
import pygame as pg


class Audio:
    def __init__(self):
        self.enabled = True
        self.ready = False
        self.sounds = {}
        self.ambient = []
        try:
            if not pg.mixer.get_init():
                pg.mixer.init(22050, -16, 1, 512)
            self.ready = True
            pg.mixer.set_num_channels(16)
            effects = {
                'jump': [(330,.065),(510,.065)], 'dash': [(160,.07),(90,.1)],
                'echo': [(880,.06),(1320,.08)], 'shard': [(523,.1),(659,.1),(784,.1),(1046,.2)],
                'checkpoint': [(392,.12),(523,.12),(784,.25)],
                'hurt': [(140,.09),(105,.1)], 'death': [(220,.1),(165,.12),(110,.2)],
                'stomp': [(170,.06),(290,.08)], 'ui': [(660,.045)],
                'portal': [(262,.14),(330,.14),(392,.14),(523,.35)],
                'shot': [(1046,.035),(660,.04)], 'shield': [(880,.07),(440,.09)],
                'block': [(220,.025),(330,.025)], 'boss': [(392,.12),(523,.12),(659,.12),(784,.3)],
            }
            for name, notes in effects.items():
                self.sounds[name] = self.make(notes, .17)
            for root in (130.81,146.83,164.81,123.47,110.):
                self.ambient.append(self.pad(root))
        except (pg.error, ValueError):
            self.ready = False

    def make(self, notes, volume):
        rate, _, channels = pg.mixer.get_init()
        samples = array('h')
        for freq, duration in notes:
            count = int(rate*duration)
            for i in range(count):
                t=i/rate
                envelope=min(1,i/(rate*.006))*max(0,1-i/count)**1.5
                val=int(32767*volume*envelope*(math.sin(math.tau*freq*t)+.2*math.sin(math.tau*freq*2*t)))
                for _ in range(channels):
                    samples.append(val)
        return pg.mixer.Sound(buffer=samples)

    def pad(self, root):
        rate, _, channels = pg.mixer.get_init()
        samples=array('h')
        duration=4
        # Integer cycles guarantee a clean loop boundary.
        freqs=[round(root*duration)/duration,round(root*1.5*duration)/duration,round(root*2*duration)/duration]
        for i in range(rate*duration):
            t=i/rate
            envelope=.4+.6*math.sin(math.pi*t/duration)**2
            val=int(32767*.027*envelope*sum(math.sin(math.tau*f*t) for f in freqs)/3)
            for _ in range(channels):
                samples.append(val)
        return pg.mixer.Sound(buffer=samples)

    def play(self, name):
        if self.ready and self.enabled and name in self.sounds:
            channel = pg.mixer.find_channel()
            if channel:
                channel.play(self.sounds[name])

    def ambience(self, index):
        if self.ready:
            pg.mixer.Channel(15).stop()
            if self.enabled:
                pg.mixer.Channel(15).play(self.ambient[index%5],loops=-1,fade_ms=700)

    def toggle(self, index):
        self.enabled=not self.enabled
        if self.ready:
            pg.mixer.stop()
        self.ambience(index)
