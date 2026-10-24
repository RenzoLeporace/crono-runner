"""Educational progression, diverse opponents and complete guardian fights."""
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
TEMP_ROOT=ROOT/'.test-tmp'
TEMP_ROOT.mkdir(exist_ok=True)
from crono.education import LESSONS,STAGES,UPGRADES,choose_question
from crono.physics import World,Controls,STEP
from crono.combat import Enemy,Projectile,Boss
from crono.save import Save,defaults


class EducationTests(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory(dir=TEMP_ROOT)
        self.save=Save(Path(self.folder.name)/'progress.json')

    def tearDown(self):
        self.folder.cleanup()

    def test_324_authored_questions_cover_every_age_and_map(self):
        self.assertEqual(len(STAGES),27)
        self.assertEqual(len(LESSONS),54)
        self.assertEqual(sum(len(l.questions) for l in LESSONS),324)
        positions=set()
        for topic,lesson in enumerate(LESSONS):
            for band in range(3):
                variants=set()
                previous=None
                for seed in range(12):
                    q=choose_question(topic,band,random.Random(seed),previous)
                    self.assertEqual(q.options[q.correct],lesson.questions[q.id%6][1])
                    self.assertEqual(len(set(q.options)),3)
                    self.assertIn(q.id%6,(band*2,band*2+1))
                    if previous is not None:
                        self.assertNotEqual(q.id,previous)
                    variants.add(q.id)
                    positions.add(q.correct)
                    previous=q.id
                self.assertEqual(len(variants),2)
        self.assertEqual(positions,{0,1,2})

    def test_revisiting_or_switching_age_cannot_duplicate_rewards(self):
        self.assertTrue(self.save.answer(0))
        self.assertEqual(self.save.data['knowledge'],2)
        self.save.data['age_band']=2
        self.assertFalse(self.save.answer(0))
        self.assertEqual(self.save.data['knowledge'],2)
        self.assertFalse(Save(self.save.path).answer(0))

    def test_buy_requirements_cost_and_no_duplicate_purchase(self):
        for i in range(10):
            self.save.answer(i)
        self.assertFalse(self.save.buy('vitality2'))
        self.assertTrue(self.save.buy('vitality'))
        self.assertEqual(self.save.data['knowledge'],17)
        self.assertFalse(self.save.buy('vitality'))
        self.assertTrue(self.save.buy('vitality2'))
        self.assertFalse(self.save.buy('unknown'))
        self.assertEqual(Save(self.save.path).data['upgrades'],['vitality','vitality2'])

    def test_all_upgrades_affordable_from_campaign_learning(self):
        for topic in range(30):
            self.save.answer(topic)
        for item in UPGRADES:
            self.assertTrue(self.save.buy(item['id']))
        self.assertEqual(len(self.save.data['upgrades']),8)
        self.assertGreater(self.save.data['knowledge'],0)

    def test_old_save_migrates_without_losing_fragments_and_backups_original(self):
        old=dict(version=1,unlocked=2,current=1,started=True,finished=False,sound=False,
                 progress=dict(index=1,checkpoint=1,shards=[0,2],echoes=[4,8]),records={})
        self.save.path.write_text(json.dumps(old),encoding='utf-8')
        migrated=Save(self.save.path)
        self.assertEqual(migrated.data['current'],3)
        self.assertEqual(migrated.data['unlocked'],6)
        w=World(1,0)
        migrated.restore(w)
        self.assertEqual(w.shards,{0,2})
        self.assertEqual(w.echoes,{4,8})
        self.assertEqual(w.checkpoint,-1)
        migrated.capture(w)
        self.assertTrue(self.save.path.with_name('progress-v1-respaldo.json').exists())
        self.assertEqual(Save(self.save.path).data['version'],4)

    def test_profile_and_upgrades_persist_on_save_restore(self):
        self.save.data.update(age_band=0,knowledge=10)
        self.save.buy('double_jump')
        self.save.answer(4)
        w=World(0,1,self.save.data['upgrades'],self.save.data['solved'])
        self.save.capture(w)
        s=Save(self.save.path)
        restored=World(0,1)
        s.restore(restored)
        self.assertEqual(s.data['age_band'],0)
        self.assertIn('double_jump',restored.player.upgrades)
        self.assertIn(4,restored.answered)


class AbilityTests(unittest.TestCase):
    def test_second_jump_only_once_until_landing(self):
        w=World(0,upgrades=['double_jump'])
        p=w.player
        p.rect.y=200
        p.grounded=False
        w.update(STEP,Controls(jump=True,held=True))
        self.assertFalse(p.air_jump)
        p.vy=100
        w.update(STEP,Controls(jump=True,held=True))
        self.assertGreater(p.vy,0)

    def test_shield_absorbs_one_hit_and_health_upgrade_applies(self):
        w=World(0,upgrades=['vitality','vitality2','shield'])
        self.assertEqual(w.player.hp,5)
        self.assertIn('shield',w.damage(200))
        self.assertEqual(w.player.hp,5)
        w.player.invincible=0
        w.damage(200)
        self.assertEqual(w.player.hp,4)
        w.respawn()
        self.assertEqual(w.player.hp,5)
        self.assertEqual(w.player.shield,1)

    def test_pulse_damage_and_armored_resistance(self):
        e=Enemy(dict(x=200,y=550,left=200,right=350,kind='armored'),0)
        self.assertFalse(e.hit(1))
        self.assertEqual(e.hp,2)
        self.assertTrue(e.hit(2))
        w=World(0,upgrades=['pulse'])
        w.update(STEP,Controls(attack=True))
        self.assertEqual(w.projectiles[0].damage,2)

    def test_enemy_archetypes_have_different_actions(self):
        w=World(0)
        w.player.rect.x=300
        for kind in ('hopper','flyer','sentry','charger'):
            e=Enemy(dict(x=320,y=550,left=200,right=600,kind=kind),0)
            e.timer=0
            old_y=e.rect.y
            e.update(STEP,w)
            if kind=='hopper':
                self.assertLess(e.rect.y,old_y)
            if kind=='flyer':
                self.assertNotEqual(e.rect.y,old_y)
            if kind=='sentry':
                self.assertTrue(w.projectiles)
            if kind=='charger':
                self.assertEqual(e.mode,'warning')

    def test_every_map_mixes_three_or_more_enemy_archetypes(self):
        geometries=set()
        for level_id in range(24):
            w=World(*divmod(level_id,3))
            self.assertGreaterEqual(len({e.kind for e in w.enemies}),3)
            geometries.add(tuple((p.rect.x,p.rect.y,p.rect.w) for p in w.platforms))
        self.assertEqual(len(geometries),24)


class GuardianTests(unittest.TestCase):
    def test_closed_core_blocks_and_knowledge_extends_opening(self):
        w=World(0,2)
        b=w.boss
        b.active=True
        b.phase='warning'
        b.hit(10)
        self.assertEqual(b.hp,b.max_hp)
        b.phase='attack'
        b.timer=0
        w.answered.add(w.level_id*2)
        b.update(STEP,w)
        self.assertEqual(b.phase,'exposed')
        self.assertGreater(b.timer,2.4)
        b.hit(2)
        self.assertEqual(b.hp,b.max_hp-2)

    def test_arena_only_starts_after_required_fragments(self):
        w=World(2,2)
        w.player.rect.midbottom=(w.data['arena_left']+180,584)
        w.update(STEP,Controls())
        self.assertFalse(w.boss.active)
        w.shards={0,1,2}
        w.update(STEP,Controls())
        self.assertTrue(w.boss.active)

    def test_death_resets_live_boss_and_keeps_learning(self):
        w=World(1,2,answered=[10])
        w.boss.hp=2
        w.boss.active=True
        w.respawn()
        self.assertEqual(w.boss.hp,w.boss.max_hp)
        self.assertFalse(w.boss.active)
        self.assertEqual(w.answered,{10})

    def test_every_guardian_can_be_defeated_without_upgrades(self):
        """Combat-only fixtures run actual AI, projectiles, damage and collisions."""
        for era in range(9):
            w=World(era,2)
            w.enemies=[]
            w.hazards=[]
            w.shards={0,1,2}
            w.player.rect.midbottom=(w.data['arena_left']+170,584)
            for tick in range(120*100):
                p=w.player
                incoming=any(s.owner=='enemy' and s.vx<0 and 0<s.rect.centerx-p.rect.centerx<115
                             and s.rect.bottom>520 and s.rect.top<584 for s in w.projectiles)
                w.update(STEP,Controls(jump=p.grounded and incoming,held=True,attack=True))
                if not w.boss.alive:
                    break
            self.assertFalse(w.boss.alive,f'Boss {era} not defeated: hp={w.boss.hp}, deaths={w.deaths}')
            self.assertEqual(w.deaths,0,f'Boss {era} combat fixture died')
            print(f'Guardian {era+1}: defeated without upgrades in {w.time:.1f}s, hp remaining {w.player.hp}')


class EducationalInterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from crono.game import Game
        cls.folder=tempfile.TemporaryDirectory(dir=TEMP_ROOT)
        cls.game=Game(True,Path(cls.folder.name)/'progress.json')

    @classmethod
    def tearDownClass(cls):
        import pygame as pg
        pg.quit()
        cls.folder.cleanup()

    def setUp(self):
        self.game.save.data=defaults()
        self.game.world=World(0)
        self.game.set_state('play')

    def test_wrong_answer_explains_without_health_or_point_penalty(self):
        g=self.game
        g.open_lesson(0)
        g.quiz_mode='question'
        before=g.world.time
        g.answer_question((g.question.correct+1)%3)
        self.assertEqual(g.quiz_mode,'wrong')
        self.assertEqual(g.world.player.hp,3)
        self.assertEqual(g.save.data['knowledge'],0)
        g.update(1)
        self.assertEqual(g.world.time,before)
        g.quiz_mode='question'
        g.answer_question(g.question.correct)
        self.assertEqual(g.save.data['knowledge'],2)

        g.quiz_mode='question'
        g.answer_question(g.question.correct)
        self.assertEqual(g.save.data['knowledge'],2)

    def test_keyboard_archive_question_answer_and_return(self):
        import pygame as pg
        g=self.game
        g.world.player.rect.midbottom=(230,584)
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_e))
        g.events()
        self.assertEqual(g.state,'quiz')
        self.assertEqual(g.quiz_mode,'read')
        g.render()
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_RETURN))
        g.events()
        self.assertEqual(g.quiz_mode,'question')
        g.render()
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_1+g.question.correct))
        g.events()
        self.assertEqual(g.quiz_mode,'correct')
        g.render()
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_RETURN))
        g.events()
        self.assertEqual(g.state,'play')
        self.assertEqual(g.save.data['knowledge'],2)

    def test_menu_age_switch_is_clickable_and_persistent(self):
        import pygame as pg
        g=self.game
        g.set_state('menu')
        g.render()
        pg.event.post(pg.event.Event(pg.MOUSEBUTTONDOWN,button=1,pos=(350,380)))
        g.events()
        self.assertEqual(g.save.data['age_band'],2)
        self.assertEqual(Save(g.save.path).data['age_band'],2)

    def test_all_educational_screens_and_age_variants_render(self):
        g=self.game
        g.save.data['discovered']=list(range(30))
        for level_id in range(24):
            g.world=World(*divmod(level_id,3))
            g.camera=900
            for state in ('play','intro','workshop','notebook','bestiary'):
                g.state=state
                g.render()
        for topic in range(30):
            for band in range(3):
                g.save.data['age_band']=band
                g.open_lesson(topic)
                for mode in ('read','question','wrong','correct'):
                    g.quiz_mode=mode
                    g.render()
                    self.assertTrue(g.buttons)
        for page in range(9):
            g.notebook_page=page
            g.state='notebook'
            g.render()


if __name__=='__main__':
    unittest.main(verbosity=2)
