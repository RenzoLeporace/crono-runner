from story_fixture import complete_story
"""New routes preserve old data; cultural visits and humanoid combat work in game."""
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
from crono.campaign import MAIN_LEVEL_IDS,successor,unlocked,rank,is_dlc,level_label
from crono.physics import World,Controls,STEP
from crono.combat import Enemy
from crono.save import Save
from crono.question_bank import QuestionBank,builtin_records
from crono.humanoid_roster import humanoid,ROLES

class ReworkTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp');self.path=Path(self.temp.name)/'progress.json'
    def tearDown(self):self.temp.cleanup()

    def test_egypt_transitions_do_not_enter_or_finish_the_dlc(self):
        s=Save(self.path)
        for level in (3,4,5):s.completed(World(*divmod(level,3)))
        self.assertEqual(s.data['current'],24)
        self.assertTrue(unlocked(24,s.data['unlocked']))
        self.assertFalse(unlocked(6,s.data['unlocked']))
        w=World(8,1);w.shards={1,2};w.checkpoint=2;s.capture(w)
        loaded=Save(self.path);target=World(8,1);loaded.restore(target)
        self.assertEqual(target.shards,{1,2});self.assertEqual(target.checkpoint,2)
        self.assertFalse(loaded.data['dlc_started'])
        for stage in range(3):loaded.completed(World(8,stage))
        self.assertEqual(loaded.data['current'],6)
        self.assertFalse(loaded.data['finished']);self.assertFalse(loaded.data['dlc_finished'])

    def test_chapter_frontiers_use_chronology_instead_of_numeric_id(self):
        self.assertEqual(len(set(MAIN_LEVEL_IDS)),24)
        for n,level in enumerate(MAIN_LEVEL_IDS):
            self.assertEqual(rank(level),n)
            self.assertFalse(is_dlc(level))
            for other in MAIN_LEVEL_IDS:self.assertEqual(unlocked(other,level),rank(other)<=n)
        self.assertEqual(successor(5),24);self.assertEqual(successor(26),6)
        self.assertEqual(successor(23),23);self.assertEqual(successor(20),20)
        self.assertEqual(level_label(24),'3.1');self.assertEqual(level_label(21),'AR.1')

    def test_v05_save_keeps_both_campaigns_enemy_damage_and_school_learning(self):
        s=Save(self.path);a=World(3,1,['shield'],[42]);a.shards={0};a.enemies[0].hp=0;a.enemies[0].alive=False
        s.data.update(unlocked=14,knowledge=7,solved=[42],discovered=[42],upgrades=['shield'])
        s.capture(a);s.capture(World(7,1,['shield'],[42]))
        raw=json.loads(self.path.read_text(encoding='utf-8'));raw['version']=3
        self.path.write_text(json.dumps(raw),encoding='utf-8')
        loaded=Save(self.path);again=World(3,1);loaded.restore(again)
        self.assertEqual(loaded.data['current'],10);self.assertEqual(loaded.data['dlc_current'],22)
        self.assertEqual(loaded.data['unlocked'],14);self.assertEqual(loaded.data['knowledge'],7)
        self.assertEqual(again.shards,{0});self.assertFalse(again.enemies[0].alive)
        self.assertIn('shield',again.upgrades);self.assertIn(42,again.answered)
        loaded.write();self.assertEqual(json.loads(self.path.with_name('progress-v3-respaldo.json').read_text()),raw)
        self.assertTrue(unlocked(24,loaded.data['unlocked']))

    def test_v05_teacher_bank_adds_egypt_without_overwriting_custom_questions(self):
        records=[q for q in builtin_records() if q['topic']<48]
        records[0].update(prompt='La pregunta de nuestra escuela',correct=2)
        records.append(dict(records[0],id=10108,prompt='Una pregunta propia'))
        self.path.write_text(json.dumps(dict(version=2,questions=records)),encoding='utf-8')
        bank=QuestionBank(self.path)
        self.assertFalse(bank.warning);self.assertEqual(len(bank.records),1297)
        self.assertEqual(bank.get(10108)['prompt'],'Una pregunta propia')
        self.assertEqual(bank.get(0)['correct'],2)
        for topic in range(48,54):
            for band in range(3):self.assertEqual(bank.choose(topic,band,random.Random(17)).topic,topic)
        bank.upsert(bank.get(10108));loaded=QuestionBank(self.path)
        self.assertEqual(len(loaded.records),1297);self.assertFalse(loaded.warning)

    def test_argentine_factions_are_human_and_preserve_patrol_floors(self):
        for stage in range(3):
            w=World(7,stage)
            factions={e.faction for e in w.enemies}
            self.assertEqual(factions,{'royalist'} if stage<2 else {'state_force','armed_cell'})
            for e,spec in zip(w.enemies,w.data['enemies']):
                self.assertNotEqual(e.kind,'flyer');self.assertEqual(e.stage,stage)
                self.assertTrue(any(p.rect.left<=e.rect.centerx<=p.rect.right and abs(p.rect.top-e.rect.bottom)<.1 for p in w.platforms))
                if e.kind=='armored' and stage==2:self.assertEqual(e.faction,'state_force')

    def test_humanoid_collision_heads_match_their_taller_models(self):
        for era,kinds in ROLES.items():
            for kind in kinds:
                e=Enemy(dict(x=450,y=550,left=300,right=700,kind=kind),era)
                self.assertEqual(e.rect.bottom,584);self.assertGreaterEqual(e.rect.h,76)
                w=World(era);w.enemies=[e];w.hazards=[]
                if kind!='armored':
                    w.player.rect.midbottom=(e.rect.centerx,e.rect.top-1);w.player.vy=250
                    events=w.update(STEP,Controls());self.assertIn('stomp',events,(era,kind))
                self.assertTrue(humanoid(era,kind))
        self.assertFalse(humanoid(0,'walker'));self.assertFalse(humanoid(1,'walker'))
        self.assertFalse(humanoid(5,'armored'));self.assertFalse(humanoid(6,'flyer'))

    def test_cultural_stops_are_on_walkable_surfaces_outside_boss_arenas(self):
        for era in (7,8):
            for stage in range(3):
                w=World(era,stage)
                for x,y,key in w.data['cultural_sites']:
                    self.assertTrue(any(p.rect.left+20<x<p.rect.right-20 and p.rect.top==y for p in w.platforms))
                    self.assertTrue(not w.boss or x<w.boss.left)
                    self.assertTrue(all(abs(x-sx)>100 for sx,sy,topic in w.data['stations']))
                from crono.curiosities import MAP_CURIOSITIES
                self.assertEqual({k for _,_,k in w.data['cultural_sites']},{MAP_CURIOSITIES[era*3+stage]})

    def test_higher_profiles_reduce_actual_checkpoints_and_keep_boss_anchor(self):
        for level in range(36):
            worlds=[World(*divmod(level,3),difficulty=band) for band in range(3)]
            counts=[len(w.checkpoint_ids) for w in worlds]
            self.assertGreaterEqual(counts[0],6);self.assertEqual(counts[1:], [4,2])
            for w in worlds:
                if w.boss:
                    last=w.checkpoint_ids[-1]
                    self.assertAlmostEqual(w.data['checkpoints'][last][0],w.boss.left+70)
                w.enemies=[];w.hazards=[]
                for i,(x,y) in enumerate(w.data['checkpoints']):
                    w.checkpoint=-1;w.player.rect.midbottom=(x,y)
                    events=w.update(STEP,Controls())
                    self.assertEqual('checkpoint' in events,i in w.checkpoint_ids)

    def test_difficulty_change_and_restore_cannot_reactivate_removed_anchor(self):
        w=World(0);removed=next(i for i in range(len(w.data['checkpoints'])) if i not in w.selected_checkpoints(2))
        w.select_checkpoint(removed);w.set_difficulty(2)
        expected=max((i for i in w.checkpoint_ids if i<=removed),default=-1)
        self.assertEqual(w.checkpoint,expected)
        s=Save(self.path);s.capture(w)
        s.data['progress']['checkpoint']=removed;s.write()
        again=World(0,difficulty=2);Save(self.path).restore(again)
        self.assertEqual(again.checkpoint,expected);self.assertEqual(again.spawn,w.spawn)
        again.respawn();self.assertEqual(again.player.rect.topleft,again.spawn)

class ReworkInterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from crono.game import Game
        cls.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp');cls.game=Game(True,Path(cls.temp.name)/'progress.json')
    @classmethod
    def tearDownClass(cls):pg.quit();cls.temp.cleanup()

    def test_cultural_interaction_pauses_and_returns_without_awarding_points(self):
        g=self.game
        for era,stage in ((7,0),(7,1),(7,2),(8,2)):
            g.world=World(era,stage);g.state='play'
            for x,y,key in g.world.data['cultural_sites']:
                g.world.player.rect.midbottom=(x,y);g.state='play';g.interact()
                self.assertEqual(g.state,'heritage');self.assertEqual(g.heritage_key,key)
                before=g.world.time;g.update(.4);g.render()
                self.assertEqual(g.world.time,before);self.assertEqual(g.save.data['knowledge'],0)
                g.close_panel();self.assertEqual(g.state,'play')

    def test_autosave_does_not_capture_an_already_completed_map(self):
        g=self.game;g.load(0,0);g.begin();g.world.shards={0,1,2}
        g.world.player.rect.midbottom=g.world.data['portal'];g.autosave=15.01
        complete_story(g.world)
        g.update(STEP)
        self.assertEqual(g.state,'complete');self.assertEqual(g.save.data['current'],1)
        self.assertIsNone(g.save.data['progress'])

    def test_detailed_landmarks_render_at_all_original_map_destinations(self):
        from crono.period_art import landmark
        g=self.game
        for era in range(7):
            images=[]
            for stage in range(3):
                w=World(era,stage);g.world=w;g.camera=w.data['zones'][2][0];g.state='play';g.render()
                self.assertGreater(len(g.buttons),0)
                img=landmark(era,stage);self.assertGreater(pg.mask.from_surface(img).count(),17000)
                images.append(pg.image.tobytes(img,'RGBA'))
            self.assertEqual(len(set(images)),3)

    def test_egypt_menu_advance_and_teacher_picker_use_actual_new_map(self):
        g=self.game;g.world=World(1,2);g.state='complete';g.render()
        g.buttons[0][1]();self.assertEqual((g.world.index,g.world.stage),(8,0))
        g.world=World(8,2);g.state='complete';g.render();g.buttons[0][1]()
        self.assertEqual((g.world.index,g.world.stage),(2,0))
        g.edit_question(2000000);g.teacher_picker=True;g.render()
        # Third chronological chapter is Egypt, while its stable internal ID is 8.
        self.assertEqual(len(g.buttons),37)
        g.buttons[6][1]();self.assertEqual(g.teacher_draft['topic']//6,8)
        g.teacher_picker=False

if __name__=='__main__':unittest.main(verbosity=2)
