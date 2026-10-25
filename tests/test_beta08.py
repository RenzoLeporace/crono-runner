"""Focused regressions for story gates, water-only journeys and wide screens."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
import wave
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.physics import World,Controls,STEP
from crono.sea_journey import SeaJourney
from crono.combat import Projectile
from story_fixture import complete_story

def sail(kind):
    sea=SeaJourney(29 if kind=='naval' else 24 if kind=='canal' else 0,kind)
    for tick in range(60*240):
        if sea.quiz:
            phase=sea.phase;hp=sea.hp;sea.answer(2)
            assert sea.phase==phase and sea.hp==hp
            sea.answer(0)
        if sea.phase==0:
            target=next((p for i,p in enumerate(sea.cargo) if i not in sea.collected),(2180,420))
        elif sea.phase==1:
            living=[e for i,e in enumerate(sea.enemies) if i not in sea.defeated]
            target=(min(living,key=lambda e:abs(e.centerx-sea.x)).left-180,min(living,key=lambda e:abs(e.centerx-sea.x)).centery+12) if len(sea.defeated)<2 else (4350,420)
        elif sea.phase==2:target=(5400,420)
        else:target=(5700,440) if sea.boss_hp else (6500,440)
        axis=0 if abs(target[0]-sea.x)<7 else 1 if target[0]>sea.x else -1
        vertical=0 if abs(target[1]-sea.y)<6 else 1 if target[1]>sea.y else -1
        sea.update(1/60,axis,vertical,True)
        if sea.finished:return sea
    raise AssertionError(f'Journey stalled: {kind}, phase {sea.phase}, position {sea.x,sea.y}, cargo {sea.collected}, defeated {sea.defeated}, boss {sea.boss_hp}')

class StoryAndWaterTests(unittest.TestCase):
    def test_fragments_alone_do_not_open_the_portal(self):
        w=World(1,0);w.enemies=[];w.hazards=[];w.shards={0,1,2};w.player.rect.midbottom=w.data['portal']
        w.update(STEP,Controls());self.assertFalse(w.complete)
        w.answered.add(w.level_id*2);w.update(STEP,Controls());self.assertFalse(w.complete)
        complete_story(w);w.answered.clear();w.update(STEP,Controls());self.assertFalse(w.complete)
        w.answered.add(w.level_id*2);w.update(STEP,Controls());self.assertTrue(w.complete)

    def test_three_maritime_routes_finish_with_actual_navigation_and_projectiles(self):
        for kind in ('naval','canal','tide'):
            with self.subTest(kind=kind):
                sea=sail(kind);self.assertTrue(sea.finished);self.assertEqual(sea.phase,3);self.assertEqual(sea.boss_hp,0)
                self.assertEqual(len(sea.collected),3);self.assertGreaterEqual(len(sea.defeated),2)
                restored=SeaJourney(sea.level,kind,state=sea.payload());self.assertEqual(restored.phase,3);self.assertEqual(restored.boss_hp,0)

    def test_no_land_map_can_mount_a_flying_boat(self):
        for level in (0,13,24,29,31):
            w=World(*divmod(level,3));m=w.mechanic;m.activate(0,0);m.activate(1,1)
            self.assertFalse(m.state['vehicle']);m.state['vehicle']=True
            w.update(STEP,Controls(held=True));self.assertFalse(m.state['vehicle'])

    def test_pulse_has_short_range_and_enemy_weapons_match_eras(self):
        shot=Projectile(100,100,680,owner='player',kind='pulse')
        for _ in range(90):
            if not shot.alive:break
            shot.update(STEP)
        self.assertFalse(shot.alive);self.assertLessEqual(shot.travelled,335)
        from crono.combat import Enemy
        expected={2:'arrow',3:'bolt',4:'rivet',5:'bullet',6:'laser',7:'musket',8:'arrow'}
        for era,kind in expected.items():
            w=World(0);e=Enemy(dict(x=300,y=550,left=250,right=600,kind='sentry'),era);e.timer=0
            e.update(STEP,w);self.assertEqual(w.projectiles[0].kind,kind)

    def test_ground_enemy_models_start_on_actual_surfaces(self):
        for level in range(46):
            w=World(*divmod(level,3))
            for e in w.enemies:
                if e.kind!='flyer':self.assertTrue(any(abs(e.rect.bottom-p.rect.top)<1 and p.rect.left<=e.rect.centerx<=p.rect.right for p in w.platforms),f'{level}: {e.kind}')

    def test_new_abilities_have_physical_effects(self):
        base=World(0);glide=World(0,upgrades=['air_brake'])
        for w in (base,glide):w.player.rect.y=150;w.player.vy=300;w.update(STEP,Controls(held=True))
        self.assertLess(glide.player.vy,base.player.vy)
        w=World(0,upgrades=['regeneration']);w.enemies=[];w.hazards=[];w.player.hp=2;w.player.recovery_clock=29.99
        w.update(.02,Controls());self.assertEqual(w.player.hp,3)
        w=World(0,upgrades=['insight']);x,y,_=w.data['stations'][0];w.player.rect.midbottom=(x-110,y)
        self.assertIsNotNone(w.near_station());w.upgrades.clear();self.assertIsNone(w.near_station())

class Interface08Tests(unittest.TestCase):
    def setUp(self):
        from crono.game import Game
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp');self.g=Game(True,Path(self.temp.name)/'save.json')
    def tearDown(self):pg.quit();self.temp.cleanup()

    def test_maritime_return_survives_restart_and_does_not_farm_rewards(self):
        from crono.save import Save
        g=self.g;g.load(8,0);g.begin();g.world.player.rect.topleft=(1500,520);g.world.player.hp=2;g.world.shards={0,2}
        g.start_voyage();g.voyage.x=2300;g.voyage.phase=1;g.persist_voyage()
        g.save=Save(g.save.path);g.set_state('menu');g.continue_game()
        self.assertEqual(g.state,'voyage');self.assertEqual(g.voyage.phase,1)
        g.voyage.phase=3;g.voyage.boss_hp=0;g.voyage.x=6500;g.voyage_update(.02)
        self.assertEqual(g.state,'play');self.assertEqual(tuple(g.world.player.rect.topleft),(1500,520));self.assertEqual(g.world.player.hp,2)
        self.assertEqual(g.world.shards,{0,2});self.assertTrue(g.world.mechanic.field.done)
        coins=g.save.data['coins'];g.start_voyage();g.leave_voyage(True);self.assertEqual(g.save.data['coins'],coins)

    def test_wide_camera_draws_more_world_without_scaling_characters(self):
        g=self.g;g.load(8,0);g.begin();g.tutorial_active=False;g.save.data['touch_controls']=True;g.world.mobile_render=True
        before=g.world.player.rect.size
        for width in (1280,1600,1920):
            g.configure_viewport(width/720);g.render()
            self.assertEqual(g.world_canvas.get_size(),(width,720));self.assertEqual(g.world.player.rect.size,before)
            self.assertNotEqual(g.world_canvas.get_at((width-10,350))[:3],(0,0,0))
        self.assertEqual(g.logical_mouse((g.ui_offset[0]+100,100)),(100,100))

    def test_mobile_scenery_is_reused_and_new_screens_render(self):
        g=self.g;g.load(8,0);g.begin();g.save.data['touch_controls']=True;g.world.mobile_render=True
        g.render();layer=g.artist.mobile_layer;g.render();self.assertIs(layer,g.artist.mobile_layer)
        for state in ('story','dlc_menu','workshop','skins'):
            g.set_state(state);g.render()
        g.skin_page=1;g.render();g.set_state('workshop');g.workshop_page=1;g.render()

    def test_original_music_decodes_and_loops(self):
        for index in range(9):
            with wave.open(str(ROOT/'assets/audio'/f'era-{index}.wav')) as f:self.assertGreaterEqual(f.getnframes()/f.getframerate(),12)
        self.g.audio.enabled=True;self.g.audio.ambience(8);self.assertTrue(pg.mixer.music.get_busy())

    def test_curriculum_filter_keeps_an_essential_question(self):
        g=self.g;g.school.config['topics']=[71];g.load(0)
        self.assertTrue(g.world.data['stations']);self.assertEqual(g.world.data['stations'][0][2],0)

if __name__=='__main__':unittest.main()
