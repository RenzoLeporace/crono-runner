"""Regressions for the requested gameplay fixes and seven new routes."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.physics import World,Controls
from crono.save import Save
from crono.sea_journey import SeaJourney

class Beta09Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from crono.game import Game
        cls.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp')
        cls.game=Game(True,Path(cls.temp.name)/'game.json')
    @classmethod
    def tearDownClass(cls):pg.quit();cls.temp.cleanup()

    def test_range_upgrade_affects_land_and_water_but_remains_bounded(self):
        for upgrades,expected in (([],330),(['long_pulse'],500)):
            w=World(0,upgrades=upgrades);w.update(.01,Controls(attack=True));shot=w.projectiles[0]
            self.assertEqual(shot.range,expected)
            while shot.alive:shot.update(1/120)
            self.assertLessEqual(shot.travelled,expected+7)
        sea=SeaJourney(0,'tide',upgrades=['long_pulse']);sea.update(.01,0,0,True)
        self.assertEqual(sea.shots[0].range,800)

    def test_maritime_hits_have_feedback_and_cannot_stack_during_protection(self):
        sea=SeaJourney(0,'tide');self.assertTrue(sea.damage());self.assertEqual(sea.hp,5)
        self.assertGreater(sea.hit_reaction,0);self.assertFalse(sea.damage());self.assertEqual(sea.hp,5)
        sea.update(.1,0,0,False);self.assertLess(sea.hit_reaction,.45)
        from crono.naval_art import vessel_image,cargo_image,draw_vessel
        target=pg.Surface((450,260));target.fill((30,91,119));draw_vessel(target,'tide',160,160,0)
        before=pg.image.tobytes(target,'RGB');target.fill((30,91,119));draw_vessel(target,'tide',160,160,0,hit=.44)
        self.assertNotEqual(before,pg.image.tobytes(target,'RGB'))
        self.assertIs(vessel_image('tide'),vessel_image('tide'));self.assertGreater(pg.mask.from_surface(cargo_image()).count(),1400)

    def test_tutorial_guides_to_the_actual_book_and_prioritizes_it(self):
        g=self.game;g.load(0);g.begin();g.tutorial_active=True;g.tutorial_step=4;g.tutorial_topic=None;g.tutorial_lesson_answered=False
        target=g.tutorial_target();g.world.player.rect.x=g.world.mechanic.devices[1][0]
        self.assertNotIn('Pulsa E',g.tutorial_instruction());g.tutorial_progress([]);self.assertTrue(g.tutorial_active)
        g.world.player.rect.midbottom=target[:2];g.world.mechanic.devices[1]=target[:2]
        self.assertIn('Pulsa E',g.tutorial_instruction());g.interact();self.assertEqual(g.state,'quiz');self.assertEqual(g.quiz_topic,target[2])
        g.quiz_mode='question';g.answer_question(g.question.correct);g.close_quiz();g.tutorial_progress([])
        self.assertFalse(g.tutorial_active);self.assertTrue(g.save.data['tutorial_done'])

    def test_one_maritime_gate_and_distinct_shore_decisions(self):
        from crono.sea_fieldwork import QUESTIONS
        g=self.game;g.tutorial_active=False
        for level in (0,24,29):
            g.load(*divmod(level,3));g.begin()
            for i in (0,1):
                g.activity_index=i;g.activity_answer(i)
                self.assertEqual(g.state,'voyage' if i==1 else 'play')
                if i==1:g.leave_voyage(False)
            prompts=[r[0] for r in QUESTIONS[g.world.mechanic.kind]];self.assertEqual(len(set(prompts)),3)

    def test_skin_purchase_needs_its_map_and_old_purchases_remain_usable(self):
        from crono.skins import buy_skin,available,SKIN_MAPS,SKINS
        save=Save(Path(self.temp.name)/'skins.json');save.data['coins']=1000
        self.assertFalse(buy_skin(save,'gaucha'));save.data['records']['36']={'score':1000}
        self.assertTrue(buy_skin(save,'gaucha'));self.assertTrue(available(Save(save.path),'gaucha'))
        save.data['purchased_skins'].append('granadero');self.assertTrue(available(save,'granadero'))
        self.assertEqual(len(SKINS),19);self.assertEqual(set(SKIN_MAPS),{s['id'] for s in SKINS if s['id']!='cronista'})

    def test_new_country_and_five_base_bonus_routes_unlock_and_persist(self):
        from crono.journeys import RESCUES
        save=Save(Path(self.temp.name)/'countries.json');self.assertTrue(save.can_enter(36));self.assertFalse(save.can_enter(37))
        save.data['records']['22']={'score':1000};self.assertTrue(save.can_enter(37))
        bonuses={v['bonus'] for v in RESCUES.values() if v['bonus']>=38};self.assertEqual(bonuses,set(range(38,43)))
        for key,row in RESCUES.items():
            if row['bonus']>=38:
                self.assertFalse(save.can_enter(row['bonus']));save.rescue(key,World(*divmod(row['level'],3)))
                self.assertTrue(Save(save.path).can_enter(row['bonus']))
        for level in range(36,46):
            w=World(*divmod(level,3));save.record_map(w);save.write()
        self.assertTrue(set(map(str,range(36,46)))<=Save(save.path).data['records'].keys())

    def test_every_new_physical_mission_can_be_completed_and_restored(self):
        for level in range(36,46):
            w=World(*divmod(level,3));w.enemies=[];m=w.mechanic;f=m.field
            for i in range(3):m.activate(i,i)
            if f.kind in ('supply','catalogue','printing','manuscripts','courier','moonrepair','dialogue'):
                for x,y in f.points:w.player.rect.midbottom=(x,y+40);f.update(.01,Controls())
            if f.kind in ('supply','catalogue','printing','dialogue','moonrepair'):
                w.player.rect.midbottom=w.data['repair_ship'] if f.kind=='moonrepair' else m.devices[0 if f.kind=='catalogue' else 2];w.player.grounded=True
                for _ in range(180):f.update(.02,Controls(work=True))
            elif f.kind=='manuscripts':
                for _ in range(3000):
                    w.player.rect.midbottom=(f.escort_x+160,f.escort_y);f.update(.05,Controls())
                    if f.done:break
            elif f.kind in ('lever','broadcast'):
                for lift in f.lifts[:2]:w.player.support=lift;f.update(.02,Controls())
            elif f.kind=='cipher':
                for x,y in f.points:
                    w.player.rect.midbottom=(x,y+40);w.player.grounded=True
                    for _ in range(200):f.update(.02,Controls(work=True))
            self.assertTrue(m.completed,f'Mission {level}: {f.description()}')
            save=Save(Path(self.temp.name)/f'mission-{level}.json');save.capture(w)
            restored=World(*divmod(level,3));Save(save.path).restore(restored);self.assertTrue(restored.mechanic.completed)

    def test_cold_coat_water_and_energy_have_real_gameplay_effects(self):
        cold=World(1,0);cold.player.rect.midbottom=(cold.traits.coat_pos[0]+300,584)
        cold.traits.update(10,Controls());self.assertLess(cold.traits.resource,100)
        cold.player.rect.midbottom=cold.traits.coat_pos;cold.traits.update(.01,Controls());self.assertTrue(cold.traits.coat)
        cold.player.rect.x+=300;before=cold.traits.resource;cold.traits.update(10,Controls());self.assertLess(cold.traits.resource,before)
        cold.traits.resource=0;cold.traits.update(.01,Controls());self.assertEqual(cold.player.hp,3);self.assertEqual(cold.checkpoint,-1)
        egypt=World(8,0);egypt.player.rect.x=5000;egypt.traits.resource=0
        egypt.traits.update(9,Controls());self.assertEqual(egypt.player.hp,2)
        egypt.player.rect.midbottom=egypt.traits.points[0];egypt.traits.update(1,Controls());self.assertGreater(egypt.traits.resource,0)
        grid=World(6,0);grid.player.rect.midbottom=grid.traits.points[0];grid.player.cooldown=1;grid.player.dash_ready=False
        grid.traits.update(.2,Controls());self.assertTrue(grid.player.dash_ready);self.assertLess(grid.player.cooldown,1)
        save=Save(Path(self.temp.name)/'coat.json');save.capture(cold);restored=World(1,0);Save(save.path).restore(restored);self.assertTrue(restored.traits.coat)

    def test_wide_controls_keep_padding_and_accept_edge_touches(self):
        from crono.touch import boxes_for_width
        g=self.game;g.configure_viewport(1600/720);g.load(0);g.begin();g.save.data['touch_controls']=True;g.tutorial_active=False
        before=[tuple(p.rect) for p in g.world.platforms];width=g.world.width
        g.render();boxes=boxes_for_width(g.viewport_width)
        self.assertEqual(boxes['left'][0],32);self.assertEqual(g.viewport_width-pg.Rect(boxes['jump']).right,32)
        for finger,action in ((71,'right'),(72,'jump')):
            box=pg.Rect(boxes[action]);g.touch_event(pg.event.Event(pg.FINGERDOWN,finger_id=finger,x=box.centerx/g.viewport_width,y=box.centery/720))
            self.assertTrue(g.touch_down(action));g.touch_event(pg.event.Event(pg.FINGERUP,finger_id=finger,x=box.centerx/g.viewport_width,y=box.centery/720))
        self.assertEqual(width,g.world.width);self.assertEqual(before,[tuple(p.rect) for p in g.world.platforms])
        g.configure_viewport(1280/720)

    def test_cold_war_order_and_lunar_traversal_without_combat(self):
        from crono.campaign import successor,chapter_levels,MAIN_LEVEL_IDS
        from route_probe import probe_route
        self.assertEqual(chapter_levels(15),(43,44,45));self.assertEqual(successor(17),43);self.assertEqual(successor(45),18)
        w=World(14,2);self.assertFalse(w.enemies);self.assertIsNone(w.boss);self.assertAlmostEqual(w.mechanic.gravity,1/6)
        self.assertLess(w.mechanic.air_control,1)
        reached,failed=probe_route(w);self.assertFalse(failed);self.assertTrue(set(w.data['main_nodes'])<=reached)
        gaps=[w.platforms[b].rect.left-w.platforms[a].rect.right for a,b in zip(w.data['main_nodes'],w.data['main_nodes'][1:])]
        self.assertGreater(max(gaps),450)
        for x,y in w.data['shards']:
            self.assertTrue(any(i in reached and p.rect.left<x<p.rect.right and 0<p.rect.top-y<60 for i,p in enumerate(w.platforms)))
        w.shards={0,1,2};w.answered.add(88);w.player.rect.midbottom=w.data['portal'];w.update(.01,Controls());self.assertFalse(w.complete)
        for i in range(3):w.mechanic.activate(i,i)
        for x,y in w.mechanic.field.points:w.player.rect.midbottom=(x,y+40);w.mechanic.field.update(.01,Controls())
        w.player.rect.midbottom=w.data['repair_ship'];w.player.grounded=True
        for _ in range(200):w.mechanic.field.update(.02,Controls(work=True))
        self.assertTrue(w.mechanic.completed);w.player.rect.midbottom=w.data['portal'];w.update(.01,Controls());self.assertTrue(w.complete)
        save=Save(Path(self.temp.name)/'moon-save.json');save.capture(w);self.assertEqual(Save(save.path).data['current'],44)
        reloaded=World(14,2);Save(save.path).restore(reloaded);self.assertTrue(reloaded.mechanic.completed)

    def test_v08_teacher_bank_migrates_without_overwriting_edits(self):
        import json
        from crono.question_bank import QuestionBank,builtin_records
        old=[r for r in builtin_records() if r['topic']<72];old[0]['prompt']='Pregunta personal conservada'
        path=Path(self.temp.name)/'old-bank.json';path.write_text(json.dumps(dict(version=4,questions=old)),encoding='utf-8')
        bank=QuestionBank(path);self.assertFalse(bank.warning);self.assertEqual(bank.get(0)['prompt'],'Pregunta personal conservada')
        self.assertEqual(len(bank.records),1800);self.assertTrue(all(any(r['topic']==t for r in bank.records) for t in range(92)))

    def test_new_scenes_and_all_era_features_render(self):
        g=self.game;g.tutorial_active=False;g.save.data['practice']=False
        for level in range(36,46):
            g.load(*divmod(level,3));g.begin();g.set_state('play');g.camera=g.world.width*.4;g.render()
        for era in range(9):
            g.load(era,0);g.begin();g.render();self.assertTrue(g.world.traits.description())
        g.set_state('dlc_menu');g.render();g.set_state('skins');g.skin_page=2;g.render()

if __name__=='__main__':unittest.main()
