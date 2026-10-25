"""Campaign separation, age-driven combat, old data and visible model variety."""
import json
import os
from pathlib import Path
import random
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.physics import World,Controls,STEP,Player
from crono.combat import Enemy,Boss
from crono.question_bank import QuestionBank,builtin_records
from crono.save import Save,defaults
from crono.education import LESSONS,STAGES

class ExpansionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp')
        self.path=Path(self.temp.name)/'progreso.json'

    def tearDown(self):self.temp.cleanup()

    def test_all_layouts_are_long_unique_and_have_required_branches(self):
        signatures=set()
        for n in range(27):
            w=World(*divmod(n,3))
            self.assertGreater(w.width,12000-1)
            signatures.add(tuple((p.rect.x,p.rect.y,p.rect.w,p.oneway) for p in w.platforms))
            self.assertGreaterEqual(len(w.data['checkpoints']),6)
            self.assertEqual(len(w.data['zones']),3)
            self.assertEqual(len(w.data['echoes']),48)
            main={w.platforms[k].rect.top for k in w.data['main_nodes']}
            self.assertGreaterEqual(len(main),3)
            for x,y in w.data['shards']:
                holders=[p for p in w.platforms if p.rect.left<=x<=p.rect.right and 20<p.rect.top-y<50]
                self.assertTrue(any(p.oneway for p in holders))
        self.assertEqual(len(signatures),27)

    def test_dlc_progress_does_not_advance_main_journey(self):
        s=Save(self.path);s.data.update(current=4,unlocked=5,started=True)
        w=World(7,0);s.capture(w)
        self.assertEqual(s.data['current'],4)
        s.completed(w)
        self.assertEqual(s.data['unlocked'],5)
        self.assertEqual(s.data['dlc_unlocked'],22)
        for stage in (1,2):s.completed(World(7,stage))
        loaded=Save(self.path)
        self.assertTrue(loaded.data['dlc_finished'])
        self.assertFalse(loaded.data['finished'])
        self.assertEqual(loaded.data['current'],4)

    def test_main_ending_is_current_era_not_argentina(self):
        s=Save(self.path)
        s.completed(World(4,2))
        self.assertFalse(s.data['finished'])
        s.completed(World(6,2))
        self.assertTrue(s.data['finished'])
        self.assertFalse(s.data['dlc_finished'])

    def test_both_in_progress_routes_restore_independently(self):
        s=Save(self.path)
        a=World(2,1);a.shards={0};a.checkpoint=2
        b=World(7,1);b.shards={1,2};b.checkpoint=3
        s.capture(a);s.capture(b)
        loaded=Save(self.path)
        aa=World(2,1);bb=World(7,1)
        loaded.restore(aa);loaded.restore(bb)
        self.assertEqual(aa.shards,{0});self.assertEqual(bb.shards,{1,2})
        self.assertEqual(aa.checkpoint,2);self.assertEqual(bb.checkpoint,3)

    def test_old_completed_campaign_opens_wars_without_erasing_learning(self):
        raw=dict(version=2,current=14,unlocked=14,finished=True,started=True,
                 knowledge=8,solved=[0,1],discovered=[0,1],upgrades=['double_jump'])
        self.path.write_text(json.dumps(raw),encoding='utf-8')
        s=Save(self.path)
        self.assertFalse(s.data['finished']);self.assertEqual(s.data['current'],15)
        self.assertEqual(s.data['knowledge'],8);self.assertEqual(s.data['upgrades'],['double_jump'])
        s.write()
        self.assertEqual(json.loads(self.path.with_name('progreso-v2-respaldo.json').read_text()),raw)

    def test_old_teacher_bank_keeps_custom_id_180_and_gains_new_topics(self):
        records=[q for q in builtin_records() if q['topic']<30]
        records[0]['prompt']='Pregunta modificada por la escuela'
        custom=dict(records[0],id=180,prompt='Pregunta adicional de la escuela')
        records.append(custom)
        self.path.write_text(json.dumps(dict(version=1,questions=records)),encoding='utf-8')
        bank=QuestionBank(self.path)
        self.assertFalse(bank.warning)
        self.assertEqual(len(bank.records),1297)
        self.assertEqual(bank.get(180)['prompt'],custom['prompt'])
        self.assertEqual(bank.get(0)['prompt'],records[0]['prompt'])
        self.assertTrue(bank.choose(47,2,random.Random(4)))
        bank.upsert(bank.get(0))
        loaded=QuestionBank(self.path)
        self.assertEqual(len(loaded.records),1297)

    def test_enemy_age_changes_speed_health_and_attack_pattern(self):
        counts=[]
        for band in range(3):
            w=World(5,difficulty=band);w.player.rect.midbottom=(400,584)
            e=Enemy(dict(x=430,y=550,left=250,right=800,kind='sentry'),5,band)
            e.timer=0;e.update(STEP,w)
            counts.append((e.speed,e.max_hp,len(w.projectiles),e.timer))
        self.assertLess(counts[0][0],counts[1][0]);self.assertLess(counts[1][0],counts[2][0])
        self.assertEqual([c[1] for c in counts],[1,2,3])
        self.assertEqual([c[2] for c in counts],[1,1,3])
        self.assertGreater(counts[0][3],counts[2][3])

    def test_upper_boss_profiles_add_telegraphs_and_shorter_windows(self):
        windows=[];health=[]
        for band in range(3):
            w=World(0,2,difficulty=band);b=w.boss
            w.player.rect.midbottom=(b.left+200,584)
            b.active=True;b.begin_attack(w)
            self.assertEqual(bool(b.telegraphs),band>0)
            health.append(b.max_hp)
            b.timer=0;b.update(STEP,w);windows.append(b.timer)
        self.assertEqual(health,sorted(health));self.assertGreater(health[2],health[0])
        self.assertGreater(windows[0],windows[1]);self.assertGreater(windows[1],windows[2])

    def test_live_profile_change_keeps_defeated_enemies_and_boss_defeated(self):
        w=World(0,2);w.enemies[0].hit(100);w.boss.alive=False;w.boss.hp=0
        w.set_difficulty(2)
        self.assertFalse(w.enemies[0].alive);self.assertEqual(w.enemies[0].hp,0)
        self.assertFalse(w.boss.alive);self.assertEqual(w.boss.hp,0)
        self.assertEqual(w.difficulty,2)

    def test_down_enters_lower_gallery_and_lands_on_next_platform(self):
        w=World(0)
        upper=next(p for p in w.platforms if p.oneway and not p.moving)
        p=w.player;p.rect.midbottom=(upper.rect.centerx,upper.rect.top)
        p.grounded=True;p.support=upper
        p.update(STEP,Controls(drop=True),w)
        self.assertGreater(p.rect.bottom,upper.rect.top)
        self.assertFalse(p.grounded)

    def test_all_54_topics_give_one_reward_including_argentina(self):
        s=Save(self.path)
        for topic in range(54):
            self.assertTrue(s.answer(topic));self.assertFalse(s.answer(topic))
        self.assertEqual(s.data['knowledge'],108)
        self.assertEqual(len(Save(self.path).data['solved']),54)

class ExpansionUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from crono.game import Game
        cls.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp')
        cls.game=Game(True,Path(cls.temp.name)/'save.json')

    @classmethod
    def tearDownClass(cls):pg.quit();cls.temp.cleanup()

    def test_age_selection_reaches_actual_world_and_live_combat(self):
        g=self.game
        for band in range(3):
            g.set_age(band);g.load(7,1)
            self.assertEqual(g.world.difficulty,band)
            self.assertTrue(all(e.difficulty==band for e in g.world.enemies))
        g.set_age(0);self.assertEqual(g.world.difficulty,0)

    def test_menu_dlc_and_atlas_keyboard_do_not_modify_main_save(self):
        g=self.game;g.save.data=defaults();g.save.data['current']=3
        g.continue_dlc();self.assertEqual(g.world.index,7)
        g.begin();g.render()
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_v));g.events()
        self.assertEqual(g.state,'atlas')
        before=g.world.time;g.update(.3);self.assertEqual(g.world.time,before)
        g.render();pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_ESCAPE));g.events()
        self.assertEqual(g.state,'play');self.assertEqual(g.save.data['current'],3)

    def test_models_have_distinct_silhouettes_not_just_colors(self):
        from crono.enemy_art import draw_enemy
        for kind in ('walker','flyer','sentry','armored'):
            masks=[]
            for era in range(9):
                s=pg.Surface((190,170),pg.SRCALPHA)
                e=Enemy(dict(x=75,y=100,left=0,right=500,kind=kind),era)
                e.rect.bottom=140
                draw_enemy(s,e,0,0,era)
                mask=pg.mask.from_surface(s)
                masks.append(bytes(mask.to_surface(setcolor=(255,255,255),unsetcolor=(0,0,0)).get_view('1')))
            self.assertEqual(len(set(masks)),9,f'{kind} silhouettes repeat')

    def test_all_new_maps_bosses_profiles_and_teacher_assignment_render(self):
        g=self.game
        for era in range(5,9):
            for band in range(3):
                g.set_age(band)
                for stage in range(3):
                    g.load(era,stage);g.camera=300;g.state='play';g.render()
                    if stage==2:
                        b=g.world.boss;b.active=True;b.begin_attack(g.world)
                        g.camera=g.world.width-1280;g.render()
        for state in ('chapters','settings','notebook','bestiary'):
            g.state=state;g.render()
        g.edit_question(10000);g.teacher_picker=True;g.render()
        self.assertEqual(len(g.buttons),37)

if __name__=='__main__':unittest.main(verbosity=2)
