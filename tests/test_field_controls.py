"""Field work must never make Crono fall through its working platform."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from collections import defaultdict
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.physics import World,Controls,STEP
from crono.game import Game
from crono.touch import boxes_for_width


def stand_at(world,point):
    floor=min((p for p in world.platforms if not p.moving and p.rect.left<=point[0]<=p.rect.right),
              key=lambda p:abs(p.rect.top-point[1]))
    floor.oneway=True
    player=world.player;player.rect.midbottom=(point[0],floor.rect.top)
    player.grounded=True;player.support=floor;player.invincible=1000
    world.enemies=[];world.hazards=[]
    return floor


class FieldControlTests(unittest.TestCase):
    def setUp(self):
        (ROOT/'.test-tmp').mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp')
        self.g=Game(True,Path(self.temp.name)/'save.json')

    def tearDown(self):
        pg.quit();self.temp.cleanup()

    def test_delivery_completes_on_a_thin_platform_without_falling(self):
        world=World(12,0);field=world.mechanic.field
        self.assertEqual(field.kind,'supply')
        world.mechanic.state['step']=3;field.collected={0,1,2}
        floor=stand_at(world,world.mechanic.devices[2])
        for _ in range(240):world.update(STEP,Controls(drop=True))
        self.assertTrue(field.done)
        self.assertEqual(world.player.rect.bottom,floor.rect.top)
        self.assertEqual(world.player.drop_time,0)

    def test_obligado_battery_can_be_coordinated_on_a_thin_platform(self):
        world=World(9,0);field=world.mechanic.field
        self.assertEqual(field.kind,'chain');world.mechanic.state['step']=3
        point=field.points[0];floor=stand_at(world,(point[0],point[1]+40))
        for _ in range(210):world.update(STEP,Controls(drop=True))
        self.assertIn(0,field.crossed)
        self.assertEqual(world.player.rect.bottom,floor.rect.top)

    def test_deliberate_descent_does_not_consume_or_trigger_double_jump(self):
        world=World(0,upgrades=['double_jump'])
        floor=next(p for p in world.platforms if p.oneway and not p.moving)
        player=world.player;player.rect.midbottom=floor.rect.midtop
        player.grounded=True;player.support=floor
        events=player.update(STEP,Controls(drop=True,jump=True,descend=True),world)
        self.assertGreater(player.rect.bottom,floor.rect.top)
        self.assertGreater(player.vy,0);self.assertNotIn('jump',events)
        self.assertTrue(player.air_jump)

    def test_keyboard_down_is_safe_and_down_plus_jump_descends(self):
        g=self.g;g.load(0);g.begin();g.tutorial_active=False
        floor=next(p for p in g.world.platforms if p.oneway and not p.moving)
        stand_at(g.world,(floor.rect.centerx,floor.rect.top))
        with patch('pygame.key.get_pressed',return_value=defaultdict(bool,{pg.K_DOWN:True})):
            g.update(1/60);self.assertEqual(g.world.player.drop_time,0)
            g.jump_pending=True;g.update(1/60)
        self.assertGreater(g.world.player.drop_time,0)
        self.assertGreater(g.world.player.rect.bottom,floor.rect.top)

    def test_android_two_finger_chord_descends_but_action_alone_does_not(self):
        g=self.g;g.configure_viewport(1600/720);g.load(0);g.begin();g.tutorial_active=False
        g.save.data['touch_controls']=True
        floor=next(p for p in g.world.platforms if p.oneway and not p.moving)
        stand_at(g.world,(floor.rect.centerx,floor.rect.top));g.render()
        def touch(action,finger):
            box=pg.Rect(boxes_for_width(1600)[action])
            g.touch_event(pg.event.Event(pg.FINGERDOWN,finger_id=finger,x=box.centerx/1600,y=box.centery/720))
        with patch('pygame.key.get_pressed',return_value=defaultdict(bool)):
            touch('drop',1);g.update(1/60)
            self.assertEqual(g.world.player.rect.bottom,floor.rect.top)
            touch('jump',2);g.update(1/60)
        self.assertGreater(g.world.player.drop_time,0)

    def test_dense_pickups_keep_every_orb_with_bounded_cosmetic_particles(self):
        g=self.g;g.load(0);g.world.enemies=[];g.world.hazards=[]
        center=g.world.player.rect.center
        g.world.data['echoes']=[center]*48
        events=g.world.update(STEP,Controls())
        self.assertEqual(events.count('echo'),48)
        for touch,budget in ((True,120),(False,240)):
            g.save.data['touch_controls']=touch;g.particles=[]
            for event in events:g.spawn_particles(event)
            self.assertLessEqual(len(g.particles),budget)
        self.assertEqual(len(g.world.echoes),48)


if __name__=='__main__':unittest.main(verbosity=2)
