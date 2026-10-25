"""Regression coverage for isolated classroom play, physical missions and rewards."""
import csv
from copy import deepcopy
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
from crono.physics import World,Controls,STEP
from crono.save import Save,defaults
from crono.school import School,rankings
from crono.rooms import Room,RoomClient
from crono.question_bank import QuestionBank,builtin_records,validate_record
from crono.field_systems import PICKUPS,LIFTS,LIGHTS,ESCORTS,HAZARDS
from crono.campaign import DISPLAY_LEVEL_IDS,DLC_LEVEL_IDS,chapter_levels,successor

class Beta07Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp');self.root=Path(self.temp.name);self.save=Save(self.root/'progreso.json')
    def tearDown(self):self.temp.cleanup()

    def test_atomic_save_retries_brief_locks_and_preserves_warning_on_failure(self):
        from unittest.mock import patch
        from crono.storage import atomic_replace
        replace=os.replace;attempts=[]
        def locked(source,target):
            attempts.append(1)
            if len(attempts)<3:raise PermissionError('temporary sync lock')
            return replace(source,target)
        self.save.data['coins']=23
        with patch('crono.storage.os.replace',side_effect=locked),patch('crono.storage.time.sleep'):
            self.save.write()
        self.assertEqual(len(attempts),3);self.assertFalse(self.save.warning)
        self.assertEqual(Save(self.save.path).data['coins'],23)
        self.save.data['coins']=24
        with patch('crono.storage.os.replace',side_effect=PermissionError('persistent lock')),patch('crono.storage.time.sleep'):
            self.save.write()
        self.assertTrue(self.save.warning);self.assertEqual(Save(self.save.path).data['coins'],23)
        self.assertTrue(self.save.path.with_suffix('.tmp').exists())

    def test_curriculum_complete_valid_random_and_teacher_migration(self):
        from collections import Counter
        rows=builtin_records();counts=Counter((q['topic'],q['band']) for q in rows)
        self.assertEqual(len(rows),1296);self.assertEqual(len(counts),216);self.assertEqual(set(counts.values()),{6})
        self.assertEqual(len({q['id'] for q in rows}),1296)
        for row in rows:validate_record(row)
        self.assertTrue({'choice','source','image','reason','chronology'}<={q.get('kind','choice') for q in rows})
        old=[deepcopy(q) for q in rows if q['topic']<54 and q['id']<5000000]
        old[0]['prompt']='Pregunta personalizada conservada'
        path=self.root/'bank.json';path.write_text(json.dumps(dict(version=3,questions=old)),encoding='utf-8')
        bank=QuestionBank(path);self.assertFalse(bank.warning);self.assertEqual(bank.get(0)['prompt'],old[0]['prompt'])
        self.assertEqual(len(bank.records),1296)

    def test_map_order_and_every_curiosity_unique(self):
        from crono.curiosities import MAP_CURIOSITIES
        self.assertEqual(len(set(DISPLAY_LEVEL_IDS)),36);self.assertEqual(chapter_levels(7),DLC_LEVEL_IDS)
        self.assertEqual(successor(22),27);self.assertEqual(successor(27),23)
        seen=[]
        for level in DISPLAY_LEVEL_IDS:
            w=World(*divmod(level,3));self.assertEqual(len(w.data['cultural_sites']),1)
            seen.append(w.data['cultural_sites'][0][2]);self.assertEqual(seen[-1],MAP_CURIOSITIES[level])
            self.assertEqual(len(set(w.mechanic.devices)),3)
        self.assertEqual(len(set(seen)),36)

    def test_practice_cannot_consume_real_progress_or_currency(self):
        w=World(7,1);w.echoes={0,1,2};w.shards={0,1};self.save.data['practice']=True
        self.save.capture(w);self.save.visit_curiosity('itati',w);self.save.rescue('san_martin',w);self.save.completed(w)
        for key in ('coins','current','unlocked'):self.assertEqual(self.save.data[key],0)
        for key in ('banked_echoes','curiosities_seen','rescued_ids','bonus_unlocked','achievements'):self.assertFalse(self.save.data[key])
        self.save.data['practice']=False;self.save.capture(w);self.save.visit_curiosity('itati',w)
        self.assertTrue(self.save.rescue('san_martin',w));self.assertEqual(self.save.data['coins'],28)
        self.save.capture(w);self.save.visit_curiosity('itati',w);self.assertFalse(self.save.rescue('san_martin',w))
        self.assertEqual(self.save.data['coins'],28)

    def test_best_score_remains_a_consistent_single_run(self):
        w=World(0);w.echoes=set(range(15));w.shards={0,1,2};w.time=45
        self.save.completed(w);record=deepcopy(self.save.data['records']['0'])
        other=World(0);other.echoes=set(range(20));other.time=999;other.deaths=10
        self.save.completed(other);self.assertEqual(self.save.data['records']['0'],record)
        self.save.capture(other);coins=self.save.data['coins'];self.save.capture(other);self.assertEqual(self.save.data['coins'],coins)

    def test_all_sixty_achievements_are_earnable_and_unlock_optional_real_bonus(self):
        from crono.achievements import earned
        from crono.achievement_catalog import CATALOG
        from crono.curiosities import MAP_CURIOSITIES
        from crono.education import UPGRADES
        from crono.skins import available
        from crono.journeys import RESCUES
        self.assertEqual(len(CATALOG),60);self.assertFalse(earned(self.save.data))
        d=self.save.data
        d.update(records={str(i):{'score':1000} for i in range(36)},fragments_by_level={str(i):[0,1,2] for i in range(36)},
            curiosities_seen=list(MAP_CURIOSITIES),banked_echoes=[f'{i}:{n}' for i in range(36) for n in range(48)],
            solved=list(range(72)),upgrades=[u['id'] for u in UPGRADES],rescued_ids=list(RESCUES),bonus_unlocked=list(range(28,33)),
            rifts_completed=[33,34,35],mechanics_completed=list(range(36)),purchased_skins=['granadero','marinero','escriba'],
            skin_cards_seen=['granadero','marinero','escriba'],metrics=dict(stomp_kills=5,dash_kills=5,shot_kills=10,
                defeated_kinds=['walker','hopper','flyer','sentry','charger','armored'],defeated_boss_eras=list(range(9)),
                boss_with_lesson=True,boss_with_two_lessons=True,level_without_death=True,boss_without_death=True))
        self.assertEqual(len(earned(d)),60);self.save.refresh_achievements();self.assertTrue(available(self.save,'cronista'))
        active=World(0,upgrades=self.save.effective_upgrades()).player.max_hp
        d['master_enabled']=False;without=World(0,upgrades=self.save.effective_upgrades()).player.max_hp
        self.assertEqual(active,without+1);self.assertTrue(available(self.save,'cronista'))

    def test_all_field_challenges_apply_physics_and_persist(self):
        for level in range(36):
            with self.subTest(level=level):
                w=World(*divmod(level,3));w.enemies=[];w.hazards=[];m=w.mechanic;f=m.field
                for i in range(3):m.activate(i,i)
                w.update(STEP,Controls());self.assertFalse(m.completed)
                if f.kind in PICKUPS or f.kind in ('race','wind','warmth'):
                    for x,y in f.points:
                        w.player.rect.midbottom=(x,y+40);w.player.vy=0;w.update(STEP,Controls())
                elif f.kind in LIFTS or f.kind in LIGHTS or f.kind in ('bridge','chain'):
                    for lift in f.lifts:
                        w.player.rect.midbottom=(lift.rect.centerx,lift.rect.top-9);w.player.vy=200;w.player.support=None;w.player.grounded=False
                        for _ in range(110):
                            w.update(STEP,Controls())
                            if w.player.support is lift:break
                elif f.kind in ESCORTS:
                    for _ in range(120*180):
                        w.player.rect.midbottom=(f.escort_x+100,f.escort_y);f.update(STEP,Controls())
                        if f.done:break
                elif f.kind in HAZARDS:
                    for x,y in m.devices[:2]:w.player.rect.midbottom=(x,y);w.update(STEP,Controls())
                    w.player.rect.midbottom=m.devices[1]
                    for _ in range(120*4):w.update(STEP,Controls())
                elif m.vehicle_kind:
                    m.state['vehicle']=True
                    for _ in range(120*4):w.update(STEP,Controls(axis=1))
                self.assertTrue(m.completed)
                self.save.capture(w);coins=self.save.data['coins'];self.save.capture(w);self.assertEqual(self.save.data['coins'],coins)
                target=World(*divmod(level,3));Save(self.save.path).restore(target)
                self.assertTrue(target.mechanic.completed);w.respawn();self.assertTrue(m.completed)

    def test_vehicle_timers_orientation_and_damage(self):
        w=World(9,2);w.enemies=[];w.hazards=[];w.mechanic.state['vehicle']=True;w.player.dash_time=.12
        w.update(STEP,Controls(axis=-1,attack=True))
        self.assertEqual(w.player.dash_time,0);self.assertEqual(w.player.facing,-1)
        self.assertTrue(any(s.owner=='player' and s.vx<0 for s in w.projectiles))
        hp=w.player.hp;w.player.invincible=0;self.assertIn('hurt',w.damage(w.player.rect.centerx+50));self.assertEqual(w.player.hp,hp-1)

    def test_field_damage_has_feedback(self):
        w=World(0,2);w.enemies=[];w.hazards=[];w.mechanic.activate(0,0)
        w.player.rect.midbottom=(450,584);w.player.invincible=0;w.mechanic.field.marks=[[w.player.rect.centerx,w.player.rect.bottom,.001]]
        self.assertIn('hurt',w.update(STEP,Controls()));self.assertEqual(w.player.hp,2)

    def test_school_files_and_nested_saves_recover_from_bad_shapes(self):
        for profiles in (None,3,[{'id':'legacy'}],[{'id':'legacy','alias':12,'role':[]}],[None,{'id':'../outside'}]):
            (self.root/'perfiles.json').write_text(json.dumps(dict(active=[],profiles=profiles)),encoding='utf-8')
            school=School(self.root);self.assertTrue(school.active['alias']);school.rows()
        bad=defaults();bad.update(metrics={'stomp_kills':['a'],'defeated_kinds':3},bonus_progress={'28':'bad'},progress={'index':0,'stage':0,'curiosities':3},records={'0':{'score':'bad'}})
        self.save.path.write_text(json.dumps(bad),encoding='utf-8');s=Save(self.save.path);w=World(0);s.restore(w);s.capture(w);s.completed(w)
        (self.root/'room.json').write_text(json.dumps(dict(members={'token':{'records':3}})),encoding='utf-8')
        room=Room(self.root/'room.json');self.assertIsInstance(room.request('/rankings',dict(token='token'))['classroom'],list)

    def test_profiles_isolated_pin_and_rankings(self):
        school=School(self.root);a=school.create('A','1A','Escuela');b=school.create('B','1B','Escuela');teacher=school.create('Profe','1A','Escuela','teacher')
        sa=school.select(a['id']);sa.data['knowledge']=9;sa.data['records']={'0':{'score':1000}};sa.write()
        sb=school.select(b['id']);self.assertEqual(sb.data['knowledge'],0);sb.data['records']={'0':{'score':500}};sb.write()
        st=school.select(teacher['id']);st.data['records']={'0':{'score':9999}};st.write()
        self.assertEqual([r['alias'] for r in rankings(school.rows(),institution='Escuela')],['A','B'])
        school.set_pin('1234');self.assertTrue(school.check_pin('1234'));self.assertFalse(school.check_pin('4321'))

    def test_rooms_real_http_scopes_duplicates_reconnect_and_practice(self):
        room=Room(self.root/'room.json');port=room.start('127.0.0.1',0)
        try:
            clients=[]
            for alias,cl,inst,role in (('A','1A','I','student'),('B','1A','I','student'),('C','1B','I','student'),('D','1A','J','student'),('Profe','1A','I','teacher')):
                client=RoomClient(f'127.0.0.1:{port}');client.call('/join',code=room.code,alias=alias,classroom=cl,institution=inst,role=role)
                client.call('/results',records={'0':{'score':1000}},practice=False);clients.append(client)
            self.assertEqual(len(clients[0].call('/rankings')['classroom']),2)
            self.assertEqual(len(clients[0].call('/rankings')['institution']),3)
            self.assertFalse(clients[0].call('/results',records={'1':{'score':8000}},practice=True)['accepted'])
            with self.assertRaises(Exception):clients[0].call('/results',records={'0':{'score':2000},'00':{'score':3000}},practice=False)
            with self.assertRaises(Exception):RoomClient(f'127.0.0.1:{port}').call('/join',code='á',alias='No')
            token=clients[0].token;clients[0].call('/join',code=room.code,alias='A',classroom='1A',institution='I');self.assertEqual(clients[0].token,token);self.assertEqual(len(room.members),5)
        finally:room.stop()

    def test_boss_feedback_only_on_actual_damage_and_after_defeat(self):
        for level in (2,5,8,11,14,17,20,23,26,27,28,29,30,31,32,33,34,35):
            w=World(*divmod(level,3));b=w.boss;b.active=True;b.phase='warning';old=b.hp;b.hit(1)
            self.assertEqual(b.hp,old);self.assertEqual(b.hit_reaction,0)
            b.phase='exposed';b.hit(1);self.assertEqual(b.hp,old-1);self.assertGreater(b.hit_reaction,0)
            b.hit_flash=0;b.hp=1;self.assertTrue(b.hit(1));self.assertFalse(b.alive);b.update(.1,w);self.assertGreater(b.hit_reaction,0)

class Beta07InterfaceTests(unittest.TestCase):
    def setUp(self):
        from crono.game import Game
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp');self.root=Path(self.temp.name);self.g=Game(True,self.root/'progreso.json')
    def tearDown(self):
        if self.g.room:self.g.room.stop()
        if self.g.room_pool:self.g.room_pool.shutdown(wait=True)
        pg.quit();self.temp.cleanup()

    def test_switching_profile_then_quitting_does_not_copy_previous_world(self):
        g=self.g;g.load(2,1);g.begin();g.world.echoes={0,1,2};g.world.shards={0,1}
        profile=g.school.create('B','Clase','Escuela');g.select_profile(profile['id']);g.running=False;g.run()
        fresh=Save(g.school.progress_path(profile['id']));self.assertFalse(fresh.data['started']);self.assertFalse(fresh.data['progress']);self.assertEqual(fresh.data['coins'],0)

    def test_rift_returns_exactly_and_completion_survives_menu_and_reload(self):
        g=self.g;g.load(7,2);g.begin();g.world.player.rect.midbottom=(5000,584);g.world.player.hp=2;g.world.shards={0,2};g.world.enemies[0].alive=False
        origin=tuple(g.world.player.rect.topleft);g.enter_rift(33);g.begin();g.save.completed(g.world)
        g.save=Save(g.save.path);g.set_state('menu');g.continue_dlc()
        self.assertEqual(g.world.level_id,23);self.assertEqual(tuple(g.world.player.rect.topleft),origin);self.assertEqual(g.world.player.hp,2)
        self.assertEqual(g.world.shards,{0,2});self.assertFalse(g.world.enemies[0].alive);self.assertIsNone(g.save.data['active_rift'])

    def test_touch_fingers_independent_and_binding_conflicts_rejected(self):
        g=self.g;g.begin();g.render()
        for finger,x,y in ((1,75/1280,610/720),(2,1190/1280,610/720)):
            g.touch_event(pg.event.Event(pg.FINGERDOWN,finger_id=finger,x=x,y=y))
        self.assertTrue(g.touch_down('left'));self.assertTrue(g.touch_down('jump'))
        g.touch_event(pg.event.Event(pg.FINGERUP,finger_id=1,x=.05,y=.85));self.assertTrue(g.touch_down('jump'));self.assertFalse(g.touch_down('left'))
        g.set_state('accessibility');g.rebind_action='left';g.binding_event(pg.event.Event(pg.KEYDOWN,key=pg.K_SPACE));self.assertEqual(g.key_for('left'),pg.K_a)

    def test_teacher_practice_unlocks_master_and_returns_from_locked_bonus(self):
        g=self.g;g.teacher_authenticated=True;g.toggle_practice();g.load(9,2);g.equip_skin('astronauta')
        self.assertIn('chronista',g.world.upgrades);self.assertTrue(all(g.save.can_enter(i) for i in range(36)))
        g.toggle_practice();self.assertEqual(g.world.level_id,0);self.assertEqual(g.save.data['skin'],'crono');self.assertFalse(g.save.data['records'])

    def test_first_attempt_and_reflection_csv_are_reconstructible(self):
        g=self.g;g.open_lesson(0);q=g.question;g.save.data['practice']=True;g.quiz_mode='question';g.answer_question(q.correct)
        g.save.data['practice']=False;g.question=q;g.quiz_mode='question';g.answer_question(q.correct)
        self.assertTrue(all(a['first'] for a in g.save.data['attempts']))
        g.open_reflection();g.reflection_field.value='Elegí esta evidencia, "porque"\nla comparé.';g.save_reflection()
        path=g.save.export_evidence(self.root/'evidence.csv',g.school.active)
        with path.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        self.assertEqual(rows[-1]['text'],'Elegí esta evidencia, "porque"\nla comparé.');self.assertEqual(rows[0]['selected_text'],q.options[q.correct])

    def test_all_new_screens_render_and_copyright_visible(self):
        for state in ('community','profile_create','room_join','teacher_access','school_settings','accessibility','activity','achievements','skins','skin_card','credits'):
            self.g.set_state(state);self.g.render()
        self.assertTrue((ROOT/'COPYRIGHT.txt').read_text(encoding='utf-8').startswith('CRONO'))

    def test_teacher_teleport_leaves_active_boss_arena(self):
        g=self.g;g.save.data['practice']=True;g.load(8,2)
        g.teacher_teleport(g.world.boss.left+180,584,True)
        g.world.update(STEP,Controls());self.assertTrue(g.world.boss.active)
        g.teacher_teleport(250,584);g.world.update(STEP,Controls())
        self.assertFalse(g.world.boss.active);self.assertLess(g.world.player.rect.centerx,400)
        g.set_state('teacher_tools');g.render()

    def test_android_import_bom_invalid_preview_and_record_limit(self):
        g=self.g;records=builtin_records()
        g.preview_native_bank(dict(text='\ufeff'+g.bank.serialise(records)))
        self.assertEqual(len(g.exchange_preview),1296)
        g.preview_native_bank(dict(text='[]'));self.assertIsNone(g.exchange_preview)
        g.preview_native_bank(dict(text=json.dumps(dict(questions=[{}]*10001))))
        self.assertIsNone(g.exchange_preview);self.assertIn('10000',g.exchange_message)

    def test_android_loads_private_progress_on_demand_and_keeps_csv_bom(self):
        from unittest.mock import patch
        from crono import mobile
        class Native:
            def loadFile(self,path):return mobile.encode_text('{"version":5,"coins":12}')
            def exportDocument(self,name,contents,mime):self.exported=mobile.decode_text(contents);return 'export'
        native=Native();fake_module=self.root/'crono'/'mobile.py';fake_module.parent.mkdir()
        with patch.object(mobile,'bridge',return_value=native),patch.object(mobile,'__file__',str(fake_module)):
            target=self.root/'saves'/'perfiles'/'test'/'progreso.json'
            mobile.ensure_file(target);self.assertEqual(json.loads(target.read_text())['coins'],12)
            csvpath=self.root/'evidencia.csv';csvpath.write_text('alias,explicación\nA,prueba',encoding='utf-8-sig')
            mobile.export_document(csvpath);self.assertTrue(native.exported.startswith('\ufeff'))
            mobile._file_jobs.clear()

    def test_android_text_transport_keeps_unicode_over_ascii_bridge(self):
        from unittest.mock import patch
        from crono import mobile
        values=['Institución · educación · ñ','\ufeffalias,explicación\nMoisés,Itatí','漢字 y 🚀']
        for value in values:
            encoded=mobile.encode_text(value);self.assertTrue(encoded.isascii())
            self.assertEqual(mobile.decode_text(encoded),value)
        class Native:
            def saveFile(self,path,contents):
                self.contents=mobile.decode_text(contents.encode('utf-8').decode('latin-1'));return True
        fake=self.root/'crono'/'mobile.py';fake.parent.mkdir()
        path=self.root/'saves'/'unicode.json';path.parent.mkdir();value=dict(institution=values[0])
        path.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8');native=Native()
        with patch.object(mobile,'bridge',return_value=native),patch.object(mobile,'__file__',str(fake)):mobile.persist(path)
        self.assertEqual(json.loads(native.contents),value)

    def test_touch_generated_mouse_does_not_open_duplicate_native_editor(self):
        from unittest.mock import patch
        g=self.g;g.set_state('profile_create');g.render();pg.event.clear()
        pg.event.post(pg.event.Event(pg.FINGERDOWN,finger_id=1,x=400/1280,y=235/720))
        pg.event.post(pg.event.Event(pg.MOUSEBUTTONDOWN,button=1,pos=(400,235),touch=True))
        with patch('crono.mobile.request_text') as request:g.events()
        self.assertEqual(request.call_count,1)

if __name__=='__main__':unittest.main()
